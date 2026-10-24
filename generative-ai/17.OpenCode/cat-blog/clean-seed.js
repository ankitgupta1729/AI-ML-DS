
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');

const prisma = new PrismaClient();

async function clearDatabase() {
  try {
    // Clear posts
    await prisma.post.deleteMany();
    
    // Clear images
    await prisma.galleryImage.deleteMany();
    
    // Clear users except admin
    await prisma.user.deleteMany({
      where: {
        email: { not: 'admin@catblog.com' }
      }
    });
    
    console.log('Database cleared');
  } catch (error) {
    console.error('Error clearing database:', error);
  } finally {
    await prisma.$disconnect();
  }
}

async function seed() {
  try {
    // Clear existing data first
    await clearDatabase();
    
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

    // Get categories first
    const catCareCategory = await prisma.category.findFirst({
      where: { slug: 'cat-care' }
    });

    if (catCareCategory) {
      console.log('Using existing cat-care category');
    } else {
      await prisma.category.create({
        data: {
          name: 'Cat Care',
          slug: 'cat-care',
          description: 'Tips and advice for taking care of your feline friends',
          color: '#10b981'
        }
      });
    }

    const catStoriesCategory = await prisma.category.findFirst({
      where: { slug: 'cat-stories' }
    });

    if (catStoriesCategory) {
      console.log('Using existing cat-stories category');
    } else {
      await prisma.category.create({
        data: {
          name: 'Cat Stories',
          slug: 'cat-stories',
          description: 'Heartwarming and funny stories about cats',
          color: '#f59e0b'
        }
      });
    }

    const catHealthCategory = await prisma.category.findFirst({
      where: { slug: 'cat-health' }
    });

    if (catHealthCategory) {
      console.log('Using existing cat-health category');
    } else {
      await prisma.category.create({
        data: {
          name: 'Cat Health',
          slug: 'cat-health',
          description: 'Health and wellness information for cats',
          color: '#ef4444'
        }
      });
    }

    console.log('Creating sample post...');
    
    const post1 = await prisma.post.create({
      data: {
        title: 'Getting Started with Your First Cat',
        slug: 'getting-started-with-your-first-cat-1',
        content: 'Getting Started with Your First Cat is an exciting experience! Here are some essential tips to get you started: Prepare Your Home Before your cat arrives, make sure you have: A comfortable bed or sleeping area, Food and water bowls, Litter box, Scratching post, Some toys for entertainment. The First Day: When you bring your cat home: Let them explore at their own pace, Show them where the litter box is, Offer food but do not force them to eat, Provide a quiet space to rest. Building Trust: Spend quality time with your new cat: Sit near them without forcing interaction, Speak softly and move slowly, Offer treats from your hand, Let them initiate contact when ready. Remember, every cat is unique and will adjust on their own schedule. Be patient and consistent, and you will build a wonderful bond!',
        excerpt: 'Essential tips for new cat owners to build a strong bond with their feline friends.',
        published: true,
        authorId: admin.id,
        categoryId: catCareCategory.id
      }
    });

    console.log('Database seeded successfully!');
    console.log('✅ Created admin user: admin@catblog.com');
    console.log('✅ Created sample post');
    console.log('✅ Database is now populated with content!');
  } catch (error) {
    console.error('Error seeding database:', error);
  } finally {
    await prisma.$disconnect();
  }
}

seed();

