'use client'

import Link from 'next/link'
import { useSession, signOut } from 'next-auth/react'
import { Button } from '@/app/ui/button'

export function Header() {
  const { data: session, status } = useSession()

  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="text-2xl font-bold text-orange-600">
              🐱 Cat Blog
            </Link>
            <nav className="ml-10 flex space-x-8">
              <Link href="/blog" className="text-gray-700 hover:text-orange-600">
                Blog
              </Link>
              <Link href="/gallery" className="text-gray-700 hover:text-orange-600">
                Gallery
              </Link>
              <Link href="/cat-of-the-day" className="text-gray-700 hover:text-orange-600">
                Cat of the Day
              </Link>
            </nav>
          </div>
          
          <div className="flex items-center space-x-4">
            {status === 'loading' ? (
              <div className="w-20 h-8 bg-gray-200 rounded animate-pulse"></div>
            ) : session ? (
              <>
                {session.user.role === 'ADMIN' && (
                  <Link href="/admin/dashboard">
                    <Button variant="outline" size="sm">
                      Admin
                    </Button>
                  </Link>
                )}
                <span className="text-sm text-gray-600">
                  {session.user.name || session.user.email}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => signOut()}
                >
                  Sign Out
                </Button>
              </>
            ) : (
              <>
                <Link href="/auth/signin">
                  <Button variant="ghost" size="sm">
                    Sign In
                  </Button>
                </Link>
                <Link href="/auth/signup">
                  <Button size="sm">
                    Sign Up
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}