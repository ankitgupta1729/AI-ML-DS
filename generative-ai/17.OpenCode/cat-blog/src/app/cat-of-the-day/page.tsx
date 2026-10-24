import { prisma } from '@/lib/prisma'
import { Header } from '../components/header'
import { Footer } from '../components/footer'

export default async function CatOfDayPage() {
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
      }
    }
  })

  // Get recent cats for archive
  const recentCats = await prisma.catOfDayFeature.findMany({
    where: { isActive: true },
    include: {
      submitter: {
        select: { id: true, name: true, username: true, avatar: true }
      }
    },
    orderBy: { featuredDate: 'desc' },
    take: 10
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">👑 Cat of the Day</h1>
          <p className="text-xl text-gray-600">
            Celebrating our feline friends, one day at a time
          </p>
        </div>

        {catOfToday ? (
          <div className="bg-white rounded-lg shadow-lg overflow-hidden mb-12">
            <div className="md:flex">
              <div className="md:w-1/2">
                <img
                  src={catOfToday.imageUrl}
                  alt={catOfToday.title}
                  className="w-full h-96 md:h-full object-cover"
                />
              </div>
              
              <div className="md:w-1/2 p-8">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-3xl font-bold text-gray-900">
                    {catOfToday.title}
                  </h2>
                  <div className="bg-orange-100 text-orange-800 px-3 py-1 rounded-full text-sm font-medium">
                    {catOfToday.voteCount} votes
                  </div>
                </div>
                
                <div className="mb-6">
                  <p className="text-gray-600 leading-relaxed whitespace-pre-wrap">
                    {catOfToday.story}
                  </p>
                </div>
                
                <div className="flex items-center justify-between border-t pt-6">
                  <div>
                    <p className="text-sm text-gray-500">
                      Submitted by {catOfToday.submitter.name || catOfToday.submitter.username}
                    </p>
                    <p className="text-xs text-gray-400">
                      {catOfToday.featuredDate.toLocaleDateString()}
                    </p>
                  </div>
                  
                  <div className="space-x-4">
                    <button className="px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors">
                      ❤️ Vote for this Cat
                    </button>
                    <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 transition-colors">
                      📤 Share
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-12 mb-12 bg-white rounded-lg shadow">
            <div className="text-6xl mb-4">🐱</div>
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">
              No Cat of the Day yet
            </h2>
            <p className="text-gray-600 mb-8">
              Check back later or submit your cat!
            </p>
          </div>
        )}

        {/* Recent Cats Archive */}
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Recent Cats</h2>
          
          {recentCats.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No cats featured yet
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recentCats.map((cat) => (
                <div key={cat.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                  <div className="h-48">
                    <img
                      src={cat.imageUrl}
                      alt={cat.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  
                  <div className="p-4">
                    <h3 className="font-semibold text-gray-900 mb-2">
                      {cat.title}
                    </h3>
                    
                    <div className="flex items-center justify-between text-sm text-gray-500">
                      <span>
                        By {cat.submitter.name || cat.submitter.username}
                      </span>
                      <span>❤️ {cat.voteCount}</span>
                    </div>
                    
                    <p className="text-xs text-gray-400 mt-1">
                      {cat.featuredDate.toLocaleDateString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Submit Cat Form */}
        <div className="mt-12 bg-white rounded-lg shadow p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Submit Your Cat</h2>
          <p className="text-gray-600 mb-6">
            Have a purrfect cat? Submit them for Cat of the Day!
          </p>
          
          <form className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Cat's Name
              </label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500"
                placeholder="What's your cat's name?"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Story
              </label>
              <textarea
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500"
                placeholder="Tell us about your cat..."
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Photo URL
              </label>
              <input
                type="url"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-orange-500 focus:border-orange-500"
                placeholder="https://example.com/cat-photo.jpg"
              />
            </div>
            
            <button
              type="submit"
              className="w-full px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors"
            >
              Submit Cat
            </button>
          </form>
        </div>
      </main>
      
      <Footer />
    </div>
  )
}