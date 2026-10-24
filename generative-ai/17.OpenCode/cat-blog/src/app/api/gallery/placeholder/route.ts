import { NextRequest, NextResponse } from 'next/server'

export async function GET() {
  const placeholderImages = [
    {
      id: '1',
      title: 'Cute Kitten',
      description: 'A tiny adorable kitten playing with yarn',
      imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Cute%20Kitten',
      createdAt: new Date().toISOString(),
      uploader: {
        name: 'Test User',
        username: 'testuser'
      },
      _count: {
        likes: 15
      },
      tags: ['cute', 'kitten']
    },
    {
      id: '2',
      title: 'Sleepy Cat',
      description: 'A cozy cat napping in a sunbeam',
      imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Sleepy%20Cat',
      createdAt: new Date(Date.now() - 86400000).toISOString(),
      uploader: {
        name: 'Test User',
        username: 'testuser'
      },
      _count: {
        likes: 23
      },
      tags: ['sleepy', 'cozy']
    },
    {
      id: '3',
      title: 'Playful Cat',
      description: 'An energetic cat jumping and playing',
      imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Playful%20Cat',
      createdAt: new Date(Date.now() - 172800000).toISOString(),
      uploader: {
        name: 'Test User',
        username: 'testuser'
      },
      _count: {
        likes: 8
      },
      tags: ['playful', 'active']
    },
    {
      id: '4',
      title: 'Mysterious Cat',
      description: 'A cat with piercing green eyes peeking around',
      imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Mysterious%20Cat',
      createdAt: new Date(Date.now() - 259200000).toISOString(),
      uploader: {
        name: 'Test User',
        username: 'testuser'
      },
      _count: {
        likes: 12
      },
      tags: ['mysterious', 'green-eyes']
    }
  ]

  return NextResponse.json(placeholderImages)
}