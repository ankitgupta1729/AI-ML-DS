export interface User {
  id: string
  email: string
  name?: string
  username: string
  avatar?: string
  bio?: string
  role: 'USER' | 'ADMIN'
  createdAt: Date
  updatedAt: Date
}

export interface Post {
  id: string
  title: string
  slug: string
  content: string
  excerpt?: string
  featuredImage?: string
  published: boolean
  createdAt: Date
  updatedAt: Date
  authorId: string
  author: User
  categoryId: string
  category: Category
  tags: Tag[]
  comments: Comment[]
  likes: Like[]
}

export interface Category {
  id: string
  name: string
  slug: string
  description?: string
  color?: string
  createdAt: Date
  updatedAt: Date
  posts: Post[]
}

export interface Tag {
  id: string
  name: string
  slug: string
  color?: string
  createdAt: Date
  posts: Post[]
}

export interface Comment {
  id: string
  content: string
  createdAt: Date
  updatedAt: Date
  authorId: string
  author: User
  postId: string
  post: Post
  parentId?: string
  parent?: Comment
  replies: Comment[]
}

export interface Like {
  id: string
  createdAt: Date
  userId: string
  user: User
  postId?: string
  post?: Post
  imageId?: string
  image?: GalleryImage
}

export interface GalleryImage {
  id: string
  title?: string
  description?: string
  imageUrl: string
  thumbnailUrl?: string
  tags?: string
  exifData?: string
  width?: number
  height?: number
  fileSize?: number
  featured: boolean
  createdAt: Date
  updatedAt: Date
  uploaderId: string
  uploader: User
  albumId?: string
  album?: Album
  likes: Like[]
}

export interface Album {
  id: string
  name: string
  slug: string
  description?: string
  coverImage?: string
  createdAt: Date
  updatedAt: Date
  images: GalleryImage[]
}

export interface CatOfDayFeature {
  id: string
  title: string
  story: string
  imageUrl: string
  featuredDate: Date
  voteCount: number
  isActive: boolean
  createdAt: Date
  updatedAt: Date
  submitterId: string
  submitter: User
  votes: Vote[]
}

export interface Vote {
  id: string
  createdAt: Date
  catOfDayFeatureId: string
  catOfDayFeature: CatOfDayFeature
  userId: string
}

export interface Subscriber {
  id: string
  email: string
  isActive: boolean
  createdAt: Date
}