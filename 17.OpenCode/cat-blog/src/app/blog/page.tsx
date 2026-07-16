import { prisma } from '@/lib/prisma'
import { Header } from '../components/header'
import { Footer } from '../components/footer'
import { Button } from '../ui/button'
import Link from 'next/link'

export default async function BlogPage() {
  const posts = await prisma.post.findMany({
    where: { published: true },
    include: {
      author: {
        select: { name: true, username: true }
      },
      category: true,
      tags: true,
      _count: {
        select: { comments: true, likes: true }
      }
    },
    orderBy: { createdAt: 'desc' },
    take: 10
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Cat Blog</h1>
          <p className="text-xl text-gray-600">
            Stories, tips, and adventures from the world of cats
          </p>
        </div>

        {posts.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">🐱</div>
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">
              No posts yet
            </h2>
            <p className="text-gray-600 mb-8">
              Be the first to share a cat story!
            </p>
            <Link href="/auth/signup">
              <Button>Join the Community</Button>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {posts.map((post) => (
              <article key={post.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                {post.featuredImage && (
                  <div className="h-48 bg-gray-200">
                    <img 
                      src={post.featuredImage} 
                      alt={post.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                )}
                
                <div className="p-6">
                  <div className="flex items-center justify-between mb-2">
                    <span 
                      className="text-xs font-medium px-2 py-1 rounded-full"
                      style={{ backgroundColor: post.category.color || '#f97316', color: 'white' }}
                    >
                      {post.category.name}
                    </span>
                    <span className="text-xs text-gray-500">
                      {post.createdAt.toLocaleDateString()}
                    </span>
                  </div>
                  
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    <Link 
                      href={`/blog/${post.slug}`}
                      className="hover:text-orange-600 transition-colors"
                    >
                      {post.title}
                    </Link>
                  </h3>
                  
                  {post.excerpt && (
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                      {post.excerpt}
                    </p>
                  )}
                  
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>By {post.author.name || post.author.username}</span>
                    <div className="flex items-center space-x-4">
                      <span>💬 {post._count.comments}</span>
                      <span>❤️ {post._count.likes}</span>
                    </div>
                  </div>
                  
                  {post.tags.length > 0 && (
                    <div className="mt-4 flex flex-wrap gap-2">
                      {post.tags.map((tag) => (
                        <span 
                          key={tag.id}
                          className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded-full"
                        >
                          {tag.name}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              </article>
            ))}
          </div>
        )}
        
        <div className="text-center mt-12">
          <Button variant="outline">Load More Posts</Button>
        </div>
      </main>
      
      <Footer />
    </div>
  )
}