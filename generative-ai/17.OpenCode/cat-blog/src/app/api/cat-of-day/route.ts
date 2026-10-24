import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/lib/auth'
import { prisma } from '@/lib/prisma'

export async function GET() {
  try {
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    const catOfToday = await prisma.catOfDayFeature.findFirst({
      where: {
        featuredDate: today,
        isActive: true
      },
      include: {
        submitter: {
          select: { id: true, name: true, username: true, avatar: true }
        },
        _count: {
          select: { votes: true }
        }
      }
    })

    // If no cat for today, get the most recent active one
    if (!catOfToday) {
      const recentCat = await prisma.catOfDayFeature.findFirst({
        where: { isActive: true },
        include: {
          submitter: {
            select: { id: true, name: true, username: true, avatar: true }
          },
          _count: {
            select: { votes: true }
          }
        },
        orderBy: { featuredDate: 'desc' }
      })

      return NextResponse.json({
        catOfToday: recentCat,
        isToday: false
      })
    }

    return NextResponse.json({
      catOfToday,
      isToday: true
    })
  } catch (error) {
    console.error('Cat of Day GET error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch cat of the day' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const session = await auth()
    
    if (!session?.user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }

    const { title, story, imageUrl } = await request.json()

    if (!title || !story || !imageUrl) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    // Check if there's already a cat for today
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    const existingToday = await prisma.catOfDayFeature.findFirst({
      where: { featuredDate: today }
    })

    if (existingToday) {
      return NextResponse.json(
        { error: 'Cat of the day already exists for today' },
        { status: 400 }
      )
    }

    const catFeature = await prisma.catOfDayFeature.create({
      data: {
        title,
        story,
        imageUrl,
        featuredDate: today,
        submitterId: session.user.id
      },
      include: {
        submitter: {
          select: { id: true, name: true, username: true, avatar: true }
        }
      }
    })

    return NextResponse.json(catFeature, { status: 201 })
  } catch (error) {
    console.error('Cat of Day POST error:', error)
    return NextResponse.json(
      { error: 'Failed to create cat of the day' },
      { status: 500 }
    )
  }
}

export async function PUT(
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

    const { action } = await request.json()

    if (action === 'vote') {
      const existingVote = await prisma.vote.findFirst({
        where: {
          catOfDayFeatureId: params.id,
          userId: session.user.id
        }
      })

      if (existingVote) {
        return NextResponse.json(
          { error: 'You have already voted for this cat' },
          { status: 400 }
        )
      }

      const vote = await prisma.vote.create({
        data: {
          catOfDayFeatureId: params.id,
          userId: session.user.id
        }
      })

      // Update vote count
      await prisma.catOfDayFeature.update({
        where: { id: params.id },
        data: {
          voteCount: {
            increment: 1
          }
        }
      })

      return NextResponse.json({ message: 'Vote recorded successfully' })
    }

    return NextResponse.json(
      { error: 'Invalid action' },
      { status: 400 }
    )
  } catch (error) {
    console.error('Cat of Day PUT error:', error)
    return NextResponse.json(
      { error: 'Failed to process request' },
      { status: 500 }
    )
  }
}