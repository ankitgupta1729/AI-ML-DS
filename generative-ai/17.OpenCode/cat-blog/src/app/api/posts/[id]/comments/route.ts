import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const session = await auth()
    
    if (!session?.user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const { content, parentId } = await request.json()

    if (!content || !content.trim()) {
      return NextResponse.json(
        { error: 'Comment content is required' },
        { status: 400 }
      )
    }

    // Verify post exists
    const post = await prisma.post.findUnique({
      where: { id: params.id }
    })

    if (!post) {
      return NextResponse.json(
        { error: 'Post not found' },
        { status: 404 }
      )
    }

    // If parentId is provided, verify it exists and belongs to the same post
    if (parentId) {
      const parentComment = await prisma.comment.findUnique({
        where: { id: parentId }
      })

      if (!parentComment || parentComment.postId !== params.id) {
        return NextResponse.json(
          { error: 'Invalid parent comment' },
          { status: 400 }
        )
      }
    }

    const comment = await prisma.comment.create({
      data: {
        content: content.trim(),
        authorId: session.user.id,
        postId: params.id,
        parentId: parentId || null
      },
      include: {
        author: {
          select: { id: true, name: true, username: true, avatar: true }
        }
      }
    })

    return NextResponse.json(comment, { status: 201 })
  } catch (error) {
    console.error('Comments POST error:', error)
    return NextResponse.json(
      { error: 'Failed to create comment' },
      { status: 500 }
    )
  }
}

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const { searchParams } = new URL(request.url)
    const page = parseInt(searchParams.get('page') || '1')
    const limit = parseInt(searchParams.get('limit') || '20')
    const skip = (page - 1) * limit

    const [comments, total] = await Promise.all([
      prisma.comment.findMany({
        where: { postId: params.id },
        include: {
          author: {
            select: { id: true, name: true, username: true, avatar: true }
          },
          replies: {
            include: {
              author: {
                select: { id: true, name: true, username: true, avatar: true }
              }
            },
            orderBy: { createdAt: 'asc' }
          }
        },
        where: { parentId: null, postId: params.id },
        orderBy: { createdAt: 'desc' },
        skip,
        take: limit
      }),
      prisma.comment.count({ where: { postId: params.id, parentId: null } })
    ])

    return NextResponse.json({
      comments,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    })
  } catch (error) {
    console.error('Comments GET error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch comments' },
      { status: 500 }
    )
  }
}