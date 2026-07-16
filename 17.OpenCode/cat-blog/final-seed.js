const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');

const prisma = new PrismaClient();

async function seed() {
  try {
    const hashedPassword = await bcrypt.hash('admin123', 12);
    
    // Create admin user
    const admin = await prisma.user.upsert({
      where: { email: 'admin@catblog.com' },
      update: {},
      create: {
        email: 'admin@catblog.com',
        username: 'admin',
        name: 'Admin User',
        password: hashedPassword,
        role: 'ADMIN'
      }
    });

    // Create sample posts
    const post1 = await prisma.post.create({
      data: {
        title: 'Getting Started with Your First Cat',
        slug: 'getting-started-with-your-first-cat',
        content: 'Getting Started with Your First Cat is an exciting experience! Here are some essential tips to get you started: Prepare Your Home Before your cat arrives, make sure you have: A comfortable bed or sleeping area, Food and water bowls, Litter box, Scratching post, Some toys for entertainment. The First Day: When you bring your cat home: Let them explore at their own pace, Show them where the litter box is, Offer food but do not force them to eat, Provide a quiet space to rest. Building Trust: Spend quality time with your new cat: Sit near them without forcing interaction, Speak softly and move slowly, Offer treats from your hand, Let them initiate contact when ready. Remember, every cat is unique and will adjust on their own schedule. Be patient and consistent, and you will build a wonderful bond!',
        excerpt: 'Essential tips for new cat owners to build a strong bond with their feline friends.',
        published: true,
        authorId: admin.id,
        categoryId: 1
      }
    });

    // Create sample gallery images
    const image1 = await prisma.galleryImage.create({
      data: {
        title: 'Sunbathing Cat',
        description: 'A cat enjoying a nap in the sun',
        imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Sunbathing Cat',
        uploaderId: admin.id,
        tags: 'sunny,relaxed'
      }
    });

    console.log('Database seeded successfully!');
    console.log('✅ Created admin user: admin@catblog.com');
    console.log('✅ Created sample blog posts and gallery images');
    console.log('✅ Database is now populated with rich content!');
  } catch (error) {
    console.error('Error seeding database:', error);
  } finally {
    await prisma.$disconnect();
  }
}

seed();