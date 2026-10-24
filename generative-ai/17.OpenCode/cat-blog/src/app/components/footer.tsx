import Link from 'next/link'

export function Footer() {
  return (
    <footer className="bg-gray-50 border-t">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-orange-600 mb-4">
              🐱 Cat Blog
            </h3>
            <p className="text-gray-600 text-sm">
              Purrfect stories, tips, and photos for cat lovers everywhere.
            </p>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Blog</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li><Link href="/blog" className="hover:text-orange-600">All Posts</Link></li>
              <li><Link href="/blog/categories" className="hover:text-orange-600">Categories</Link></li>
              <li><Link href="/blog/tags" className="hover:text-orange-600">Tags</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Community</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li><Link href="/gallery" className="hover:text-orange-600">Photo Gallery</Link></li>
              <li><Link href="/cat-of-the-day" className="hover:text-orange-600">Cat of the Day</Link></li>
              <li><Link href="/subscribe" className="hover:text-orange-600">Newsletter</Link></li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-medium text-gray-900 mb-3">Connect</h4>
            <ul className="space-y-2 text-sm text-gray-600">
              <li><Link href="/about" className="hover:text-orange-600">About</Link></li>
              <li><Link href="/contact" className="hover:text-orange-600">Contact</Link></li>
              <li><Link href="/privacy" className="hover:text-orange-600">Privacy</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t mt-8 pt-8 text-center text-sm text-gray-500">
          <p>&copy; 2024 Cat Blog. Made with ❤️ for cat lovers.</p>
        </div>
      </div>
    </footer>
  )
}