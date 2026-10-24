import Link from 'next/link'
import { Header } from './components/header'
import { Footer } from './components/footer'
import { Button } from './ui/button'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main>
        {/* Hero Section */}
        <section className="bg-gradient-to-r from-orange-50 to-white py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Welcome to <span className="text-orange-600">Cat Blog</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Purrfect stories, care tips, and adorable photos for cat lovers everywhere. 
              Join our community of feline enthusiasts!
            </p>
            <div className="space-x-4">
              <Link href="/blog">
                <Button size="lg">
                  Read Stories
                </Button>
              </Link>
              <Link href="/gallery">
                <Button variant="outline" size="lg">
                  View Gallery
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
              Explore Our Features
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-4xl mb-4">📝</div>
                <h3 className="text-xl font-semibold mb-2">Cat Stories</h3>
                <p className="text-gray-600">
                  Heartwarming tales and adventures from cat owners around the world.
                </p>
              </div>
              <div className="text-center">
                <div className="text-4xl mb-4">📸</div>
                <h3 className="text-xl font-semibold mb-2">Photo Gallery</h3>
                <p className="text-gray-600">
                  Share and browse adorable cat photos in our community gallery.
                </p>
              </div>
              <div className="text-center">
                <div className="text-4xl mb-4">👑</div>
                <h3 className="text-xl font-semibold mb-2">Cat of the Day</h3>
                <p className="text-gray-600">
                  Vote for your favorite cats and discover new furry friends daily.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Recent Posts Preview */}
        <section className="py-20 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
              Latest from the Blog
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="h-40 bg-gray-200 rounded mb-4"></div>
                <h3 className="text-lg font-semibold mb-2">Coming Soon</h3>
                <p className="text-gray-600 text-sm">
                  Stay tuned for amazing cat content!
                </p>
              </div>
              <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="h-40 bg-gray-200 rounded mb-4"></div>
                <h3 className="text-lg font-semibold mb-2">Coming Soon</h3>
                <p className="text-gray-600 text-sm">
                  More purrfect articles on the way!
                </p>
              </div>
              <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
                <div className="h-40 bg-gray-200 rounded mb-4"></div>
                <h3 className="text-lg font-semibold mb-2">Coming Soon</h3>
                <p className="text-gray-600 text-sm">
                  Exciting cat stories await!
                </p>
              </div>
            </div>
            <div className="text-center mt-8">
              <Link href="/blog">
                <Button variant="outline">
                  View All Posts
                </Button>
              </Link>
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  )
}
