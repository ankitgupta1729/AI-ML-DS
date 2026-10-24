# 🐱 Cat Blog

A full-stack cat blog website built with Next.js, TypeScript, Prisma, and Tailwind CSS. Features include blog posts, photo galleries, user authentication, and a "Cat of the Day" feature.

## ✨ Features

### 🌟 Core Features
- **Blog System**: Create, read, update, and delete blog posts with categories and tags
- **User Authentication**: Secure login/signup system with role-based access (User/Admin)
- **Admin Dashboard**: Complete admin interface for managing content
- **Commenting System**: Nested comments with moderation capabilities
- **Photo Gallery**: Upload and browse cat photos with albums
- **Cat of the Day**: Daily featured cats with voting system

### 🎨 Design & UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Modern UI**: Clean, cat-themed design with orange color scheme
- **Interactive Elements**: Hover effects, smooth transitions, and micro-interactions
- **SEO Optimized**: Meta tags, structured data, and semantic HTML

### 🔧 Technical Features
- **TypeScript**: Full type safety throughout the application
- **Database**: SQLite with Prisma ORM (easily switchable to PostgreSQL)
- **Authentication**: NextAuth.js with credential-based login
- **File Upload**: Image upload with validation and optimization
- **API Routes**: RESTful API for all features

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

1. **Clone and setup**
   ```bash
   git clone <your-repo-url>
   cd cat-blog
   npm install
   ```

2. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Database setup**
   ```bash
   npx prisma migrate dev
   npx prisma generate
   ```

4. **Run development server**
   ```bash
   npm run dev
   ```

5. **Visit app**
   Open [http://localhost:3000](http://localhost:3000) in your browser

## 📁 Project Structure

```
cat-blog/
├── src/app/                    # Next.js App Router
│   ├── (auth)/                # Authentication pages (signin, signup)
│   ├── (admin)/               # Admin dashboard
│   ├── api/                   # API routes
│   ├── blog/                  # Blog pages
│   ├── gallery/               # Photo gallery
│   ├── cat-of-the-day/        # Cat of the Day feature
│   ├── components/            # Reusable React components
│   ├── ui/                   # UI components (Button, etc.)
│   ├── lib/                  # Utilities and configurations
│   └── types/                # TypeScript type definitions
├── prisma/                   # Database schema and migrations
├── public/                   # Static assets
└── uploads/                  # User-uploaded files
```

## 🗄️ Database Schema

The application uses a comprehensive database schema with the following models:

- **Users**: Authentication and user profiles
- **Posts**: Blog posts with rich content
- **Categories & Tags**: Content organization
- **Comments**: Nested commenting system
- **Gallery Images**: Photo management
- **Albums**: Photo collections
- **Cat of the Day**: Daily featured cats
- **Votes**: Voting system
- **Subscribers**: Newsletter subscriptions

## 🔐 Authentication

Uses NextAuth.js for secure authentication:
- Credential-based login (email/password)
- Role-based access control (USER/ADMIN)
- Protected routes and API endpoints
- Session management

## 📸 Gallery Features

- **Image Upload**: Secure file upload with validation
- **Image Optimization**: Automatic thumbnail generation
- **Albums**: Organize photos into collections
- **EXIF Data**: Store and display photo metadata
- **Likes System**: User engagement with photos

## 👑 Cat of the Day

- **Daily Selection**: New featured cat each day
- **Voting System**: Users can vote for favorites
- **Archive**: Browse previous featured cats
- **Submission Form**: Easy cat submission process

## 🛠️ Development

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check    # Run TypeScript type checking
```

### Database Management

```bash
npx prisma studio    # Open database GUI
npx prisma migrate dev # Run database migrations
npx prisma generate   # Generate Prisma client
```

## 🌟 Key Features Implementation

### Admin Dashboard
- Content management (posts, categories, users)
- Analytics and statistics
- Comment moderation
- Media library management

### Blog System
- Rich text editing capabilities
- SEO-friendly URLs
- Category and tag organization
- Draft/published states

### User Experience
- Responsive mobile-first design
- Smooth animations and transitions
- Loading states and error handling
- Search and filtering capabilities

## 📱 Responsive Design

The application is fully responsive with breakpoints for:
- Mobile: < 768px
- Tablet: 768px - 1024px  
- Desktop: > 1024px

## 🚀 Deployment

The application is ready for deployment on:
- **Vercel** (recommended)
- **Netlify**
- **AWS Amplify**
- **Any platform supporting Next.js**

### Environment Variables for Production

```
DATABASE_URL=              # Production database URL
NEXTAUTH_URL=             # Your production URL
NEXTAUTH_SECRET=          # Secret key for NextAuth
```

## 🎯 Future Enhancements

- Social media integration
- Email notifications
- Advanced search functionality
- Dark mode support
- Real-time comments
- Image AI tagging
- Mobile app companion

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙋‍♂️ Support

For questions or support, please open an issue in the repository.

---

Built with ❤️ for cat lovers everywhere! 🐱
