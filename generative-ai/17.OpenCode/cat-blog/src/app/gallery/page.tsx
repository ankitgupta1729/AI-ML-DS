'use client'

import { useState } from 'react'
import { Header } from '../components/header'
import { Footer } from '../components/footer'

export default function GalleryPage() {
  const [isUploading, setIsUploading] = useState(false)

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsUploading(true)

    try {
      const formData = new FormData(e.currentTarget)
      const fileInput = e.currentTarget.querySelector('input[type="file"]') as HTMLInputElement
      
      if (!fileInput.files?.[0]) {
        alert('Please select a file to upload')
        return
      }

      const file = fileInput.files[0]
      formData.append('file', file)

      const response = await fetch('/api/gallery/upload', {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        alert('Photo uploaded successfully!')
        window.location.reload()
      } else {
        const error = await response.json()
        alert(`Upload failed: ${error.error}`)
      }
    } catch (error) {
      alert(`Upload failed: ${error.message}`)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Cat Gallery</h1>
          <p className="text-xl text-gray-600 mb-8">
            Adorable photos of our feline friends shared by the community
          </p>
        </div>

        {/* Upload Form */}
        <div className="max-w-2xl mx-auto mb-12">
          <form onSubmit={handleUpload} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Upload a Cat Photo
              </label>
              <div className="space-y-4">
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/gif,image/webp"
                  required
                  className="block w-full text-sm text-gray-900 border-gray-300 rounded-md p-3 focus:ring-orange-500 focus:border-orange-500 file:mr-4 file:mt-0 block w-full text-sm text-gray-900 border-gray-300 rounded-md p-3"
                />
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input
                    type="text"
                    name="title"
                    placeholder="Give your cat a title..."
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500"
                  />
                  <input
                    type="text"
                    name="description"
                    placeholder="Tell us about this photo..."
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500"
                  />
                  <input
                    type="text"
                    name="tags"
                    placeholder="Tags (comma separated)..."
                    className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-orange-500 focus:border-orange-500"
                  />
                </div>
              </div>
              
              <button
                type="submit"
                disabled={isUploading}
                className="w-full px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
              >
                {isUploading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-orange-600 border-t-transparent"></div>
                    <span className="ml-2">Uploading...</span>
                  </>
                ) : (
                  'Upload Photo'
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Gallery Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {[1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
            <div key={i} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
              <div className="aspect-square bg-gray-200">
                <img 
                  src={`/api/gallery/placeholder?width=400&height=400`} 
                  alt={`Sample cat photo ${i}`}
                  className="w-full h-full object-cover"
                />
              </div>
              
              <div className="p-4">
                <h3 className="font-medium text-gray-900 mb-2 truncate">
                  Adorable Cat {i}
                </h3>
                
                <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                  This is a placeholder for a beautiful cat photo. In the real application, this would show an actual uploaded image of a cat with a cute expression, doing something adorable like napping, playing, or begging for treats.
                </p>
                
                <div className="flex items-center justify-between text-sm text-gray-500">
                  <span>Community Member</span>
                  <span>❤️ {10 + i}</span>
                </div>
                
                <div className="mt-2 flex flex-wrap gap-1">
                  <span className="text-xs bg-orange-100 text-orange-800 px-2 py-1 rounded-full">
                    cute
                  </span>
                  <span className="text-xs bg-pink-100 text-pink-800 px-2 py-1 rounded-full">
                    playful
                  </span>
                  <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                    sleepy
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <div className="text-center mt-12">
          <button className="px-6 py-3 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors">
            Load More Photos
          </button>
        </div>
      </main>
      
      <Footer />
    </div>
  )
}