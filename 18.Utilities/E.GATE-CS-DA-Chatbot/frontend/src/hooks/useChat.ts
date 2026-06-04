import { useCallback, useRef, useState } from "react";
import {
  streamChat,
  streamRegenerate,
  submitFeedback,
  type FeedbackInput,
  type HistoryTurn,
} from "../lib/api";
import type {
  Attachment,
  ChatMessage,
  DonePayload,
  Rating,
  SendOpts,
} from "../types";

const uid = () =>
  `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const convRef = useRef<string | null>(null);

  const stop = useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
    setIsStreaming(false);
    setMessages((prev) =>
      prev.map((m) => (m.streaming ? { ...m, streaming: false } : m)),
    );
  }, []);

  const clear = useCallback(() => {
    stop();
    convRef.current = null;
    setMessages([]);
  }, [stop]);

  const patchById = useCallback(
    (id: string, fn: (m: ChatMessage) => ChatMessage) =>
      setMessages((prev) => prev.map((m) => (m.id === id ? fn(m) : m))),
    [],
  );

  // Shared streaming wiring for both new answers and regenerations.
  const runStream = useCallback(
    (
      botId: string,
      start: (cb: {
        onToken: (t: string) => void;
        onDone: (p: DonePayload) => void;
        onError: (msg: string) => void;
        signal: AbortSignal;
      }) => Promise<void>,
    ) => {
      setIsStreaming(true);
      const controller = new AbortController();
      abortRef.current = controller;

      start({
        signal: controller.signal,
        onToken: (tok) =>
          patchById(botId, (m) => ({ ...m, content: m.content + tok })),
        onDone: (p) => {
          if (p.conversationId) convRef.current = p.conversationId;
          patchById(botId, (m) => ({
            ...m,
            sources: p.sources,
            inScope: p.inScope,
            messageId: p.messageId,
            confidence: p.confidence,
            streaming: false,
          }));
          setIsStreaming(false);
          abortRef.current = null;
        },
        onError: (msg) => {
          patchById(botId, (m) => ({
            ...m,
            content: m.content || `⚠️ ${msg}`,
            error: true,
            streaming: false,
          }));
          setIsStreaming(false);
          abortRef.current = null;
        },
      });
    },
    [patchById],
  );

  const send = useCallback(
    (question: string, attachments: Attachment[] = [], opts: SendOpts = {}) => {
      const text = question.trim();
      if ((!text && attachments.length === 0) || isStreaming) return;

      const history: HistoryTurn[] = messages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const userMsg: ChatMessage = {
        id: uid(),
        role: "user",
        content: text,
        attachments: attachments.length ? attachments : undefined,
      };
      const botId = uid();
      const botMsg: ChatMessage = {
        id: botId,
        role: "assistant",
        content: "",
        streaming: true,
        rating: null,
      };
      setMessages((prev) => [...prev, userMsg, botMsg]);

      runStream(botId, (cb) =>
        streamChat(
          text || "(see attachment)", history, convRef.current, attachments, cb, opts,
        ),
      );
    },
    [messages, isStreaming, runStream],
  );

  const regenerate = useCallback(
    (clientId: string, opts: SendOpts = {}) => {
      if (isStreaming) return;
      const idx = messages.findIndex((m) => m.id === clientId);
      if (idx < 0) return;
      const target = messages[idx];

      // Reset the bubble and stream a fresh answer into it.
      patchById(clientId, (m) => ({
        ...m,
        content: "",
        sources: undefined,
        error: false,
        rating: null,
        feedbackSent: false,
        streaming: true,
      }));

      if (target.messageId) {
        runStream(clientId, (cb) =>
          streamRegenerate(target.messageId as string, null, cb, opts),
        );
      } else {
        // No server id (DB off) → resend the preceding user question.
        const prevUser = [...messages.slice(0, idx)]
          .reverse()
          .find((m) => m.role === "user");
        const history: HistoryTurn[] = messages
          .slice(0, idx)
          .map((m) => ({ role: m.role, content: m.content }));
        if (!prevUser) return;
        runStream(clientId, (cb) =>
          streamChat(
            prevUser.content,
            history.slice(0, -1),
            convRef.current,
            [],
            cb,
            opts,
          ),
        );
      }
    },
    [messages, isStreaming, patchById, runStream],
  );

  const sendFeedback = useCallback(
    async (
      clientId: string,
      rating: Rating,
      extra?: { reason?: string; comment?: string; correctedAnswer?: string },
    ) => {
      const msg = messages.find((m) => m.id === clientId);
      if (!msg) return;
      // Optimistic UI: toggle off if clicking the same rating again.
      const next = msg.rating === rating ? null : rating;
      patchById(clientId, (m) => ({ ...m, rating: next, feedbackSent: true }));

      if (msg.messageId && next) {
        const payload: FeedbackInput = {
          messageId: msg.messageId,
          rating: next,
          reason: extra?.reason,
          comment: extra?.comment,
          correctedAnswer: extra?.correctedAnswer,
        };
        await submitFeedback(payload);
      }
    },
    [messages, patchById],
  );

  return {
    messages,
    isStreaming,
    send,
    stop,
    clear,
    regenerate,
    sendFeedback,
  };
}
