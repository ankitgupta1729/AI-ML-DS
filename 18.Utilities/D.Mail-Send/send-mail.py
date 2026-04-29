"""
Send a beautifully formatted teaser email that links to a hosted
interactive love letter (letter.html) where the real magic lives.

WHY THIS DESIGN
---------------
Gmail strips JavaScript, blocks <form> submits, and ignores most
animations. Anything truly INTERACTIVE has to live on a web page.

So this script sends an elegant teaser email with a "Open Your Letter"
button. The button links to your hosted letter.html — where she'll see
a sealed envelope, a typewriter intro, and three decoder puzzles she
actually clicks and solves.

SETUP (one-time)
----------------
A. Host letter.html somewhere with a public URL. Easy free options:
     - GitHub Pages    (push to a repo, enable Pages)
     - Netlify Drop    (https://app.netlify.com/drop, drag the file)
     - Vercel          (vercel deploy)
   Whatever you use, copy the final URL and paste it as LETTER_URL below.

B. Gmail App Password (NOT your regular password):
     1. Turn on 2-Step Verification:
        https://myaccount.google.com/security
     2. Generate an App Password:
        https://myaccount.google.com/apppasswords
        App: "Mail", Device: "Other" -> name it "Python Script"
     3. Set it as an env var:

          macOS / Linux:
            export GMAIL_APP_PASSWORD="abcd efgh ijkl mnop"

          Windows (PowerShell):
            $env:GMAIL_APP_PASSWORD="abcd efgh ijkl mnop"

C. Run:
     python send_love_email.py
"""

import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

# =============================================================================
# CONFIG
# =============================================================================
SENDER_EMAIL   = "ankitgupta1729@gmail.com"
RECEIVER_EMAIL = "Neha.Patel@crowe.com"
SENDER_NAME    = "Ankit"

# >>> IMPORTANT: replace this with your hosted letter.html URL <<<
LETTER_URL = "loquacious-stroopwafel-3e4d90.netlify.app"

APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")

SUBJECT = "I made you something. Open when you have a quiet minute  \u2727"


# =============================================================================
# HTML EMAIL (Gmail-safe teaser that drives her to the interactive page)
# =============================================================================
HTML_BODY = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>For You</title>
</head>
<body style="margin:0; padding:0; background:#1a0d12; font-family: Georgia, 'Times New Roman', serif;">

<!-- Preheader: the inbox preview line -->
<div style="display:none; max-height:0; overflow:hidden; opacity:0; color:#1a0d12;">
  A sealed letter. Three secrets. Open when you can.
</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
       style="background: #1a0d12;">
  <tr>
    <td align="center" style="padding: 48px 16px;">

      <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"
             style="max-width:600px; width:100%; background: #fffaf3;
                    border-radius: 6px; overflow: hidden;
                    box-shadow: 0 16px 48px rgba(0,0,0,0.4);">

        <!-- ===== Header band ===== -->
        <tr>
          <td style="background: linear-gradient(135deg, #5e1e32 0%, #8a3548 60%, #b85c70 100%);
                     padding: 64px 40px 56px 40px; text-align:center;">
            <p style="margin:0 0 18px 0; color:#f5d6c0; font-family: Georgia, serif;
                      font-size:11px; letter-spacing:6px; text-transform:uppercase;">
              &#10022; &nbsp; A Sealed Letter &nbsp; &#10022;
            </p>
            <h1 style="margin:0; color:#fffaf3; font-family: Georgia, 'Times New Roman', serif;
                       font-size:38px; font-weight:normal; font-style:italic;
                       letter-spacing:1px; line-height:1.25;">
              for the one<br>
              who reads me<br>
              without a word.
            </h1>
            <p style="margin:28px 0 0 0; color:#f5d6c0; font-family: Georgia, serif;
                      font-size:13px; letter-spacing:3px;">
              &#10086; &nbsp; &nbsp; &#10086; &nbsp; &nbsp; &#10086;
            </p>
          </td>
        </tr>

        <!-- ===== Wax seal envelope (decorative SVG-free, table-built) ===== -->
        <tr>
          <td align="center" style="padding: 48px 40px 24px 40px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="position:relative; width: 200px; height: 140px;
                           background: linear-gradient(135deg, #5e1e32 0%, #8a3548 100%);
                           border-radius: 4px; text-align:center; vertical-align:middle;
                           font-family: Georgia, serif; font-style: italic;
                           font-size: 32px; color: #d4a574;
                           box-shadow: 0 8px 24px rgba(94, 30, 50, 0.25);">
                  &#10086;
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ===== Body ===== -->
        <tr>
          <td style="padding: 16px 56px 8px 56px; text-align:center;">
            <p style="margin:0 0 18px 0; color:#8a3548; font-family: Georgia, serif;
                      font-style:italic; font-size:20px;">
              Hello, you.
            </p>
            <p style="margin:0 0 18px 0; color:#3a2228; font-family: Georgia, serif;
                      font-size:17px; line-height:1.85;">
              I was going to send a regular text. Then I thought &mdash; no.
              You deserve something you can actually <em>open</em>.
            </p>
            <p style="margin:0; color:#3a2228; font-family: Georgia, serif;
                      font-size:17px; line-height:1.85;">
              So I built you a letter. It&rsquo;s sealed,<br>
              and there are three small puzzles inside.<br>
              Solve them, and you&rsquo;ll find what I keep meaning to say.
            </p>
          </td>
        </tr>

        <!-- ===== Ornament divider ===== -->
        <tr>
          <td align="center" style="padding: 28px 56px 16px 56px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="border-top: 1px solid #d9b8a8; width: 60px;
                           font-size:0; line-height:0;">&nbsp;</td>
                <td style="padding: 0 14px; color:#b85c70; font-family: Georgia, serif;
                           font-size:18px;">&#10086;</td>
                <td style="border-top: 1px solid #d9b8a8; width: 60px;
                           font-size:0; line-height:0;">&nbsp;</td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- ===== CTA button (bulletproof table-based, no <button> tag) ===== -->
        <tr>
          <td align="center" style="padding: 16px 40px 32px 40px;">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td align="center" bgcolor="#5e1e32"
                    style="border-radius: 4px;
                           background: linear-gradient(135deg, #5e1e32 0%, #8a3548 100%);">
                  <a href="{LETTER_URL}"
                     style="display:inline-block; padding: 18px 44px;
                            font-family: Georgia, serif; font-size: 14px;
                            letter-spacing: 4px; text-transform: uppercase;
                            color: #fffaf3; text-decoration: none;
                            border-radius: 4px;">
                    &#10022; &nbsp; Open Your Letter &nbsp; &#10022;
                  </a>
                </td>
              </tr>
            </table>
            <p style="margin: 18px 0 0 0; color:#8a6a6a; font-family: Georgia, serif;
                      font-size:13px; font-style:italic;">
              best opened with a cup of something warm
            </p>
          </td>
        </tr>

        <!-- ===== Signature ===== -->
        <tr>
          <td style="padding: 16px 56px 56px 56px; text-align:center;">
            <p style="margin:0 0 6px 0; color:#8a3548; font-family: Georgia, serif;
                      font-style:italic; font-size:14px;">
              Yours,
            </p>
            <p style="margin:0; color:#5e1e32;
                      font-family: Georgia, 'Times New Roman', serif;
                      font-size:34px; font-style:italic; font-weight:normal;">
              {SENDER_NAME}
            </p>
          </td>
        </tr>

        <!-- ===== Footer band ===== -->
        <tr>
          <td style="background:#3a2228; padding: 22px 40px; text-align:center;">
            <p style="margin:0; color:#d9b8a8; font-family: Georgia, serif;
                      font-size:11px; letter-spacing:3px;">
              &#10086; &nbsp; sent with intention &nbsp; &#10086;
            </p>
          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>

</body>
</html>
"""


# =============================================================================
# Plain-text fallback (improves deliverability, shown if HTML can't render)
# =============================================================================
TEXT_BODY = f"""\
Hello, you.

I was going to send a regular text. Then I thought - no. You deserve
something you can actually open.

So I built you a letter. It is sealed, and there are three small puzzles
inside. Solve them, and you'll find what I keep meaning to say.

Open your letter:
{LETTER_URL}

Best opened with a cup of something warm.

Yours,
{SENDER_NAME}
"""


# =============================================================================
# SEND
# =============================================================================
def send_email() -> None:
    if not APP_PASSWORD:
        raise SystemExit(
            "\nERROR: GMAIL_APP_PASSWORD environment variable is not set.\n"
            "See the setup instructions at the top of this file.\n"
        )

    if "your-hosted-letter.example.com" in LETTER_URL:
        print(
            "\nWARNING: LETTER_URL is still the placeholder.\n"
            "Edit this file and paste your real hosted URL for letter.html\n"
            "before sending. Aborting.\n"
        )
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"]    = formataddr((SENDER_NAME, SENDER_EMAIL))
    msg["To"]      = RECEIVER_EMAIL

    msg.attach(MIMEText(TEXT_BODY, "plain", "utf-8"))
    msg.attach(MIMEText(HTML_BODY, "html",  "utf-8"))

    context = ssl.create_default_context()

    print("Connecting to Gmail...")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        print("Logged in. Sending email...")
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())

    print(f"\nDone. Email delivered to {RECEIVER_EMAIL}.")


if __name__ == "__main__":
    send_email()