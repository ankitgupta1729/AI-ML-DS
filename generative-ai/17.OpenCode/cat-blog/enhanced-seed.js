
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

    // Create more users
    const userPassword = await bcrypt.hash('user123', 12);
    for (let i = 1; i <= 3; i++) {
      await prisma.user.create({
        data: {
          email: `user${i}@example.com`,
          username: `catlover${i}`,
          name: `Cat Lover ${i}`,
          password: userPassword,
          role: 'USER'
        }
      });
    }

    const catCareCategory = await prisma.category.findFirst({
      where: { slug: 'cat-care' }
    });

    const catStoriesCategory = await prisma.category.findFirst({
      where: { slug: 'cat-stories' }
    });

    const catHealthCategory = await prisma.category.findFirst({
      where: { slug: 'cat-health' }
    });

    // Create multiple sample posts
    const posts = [
      {
        title: 'Getting Started with Your First Cat',
        slug: 'getting-started-with-your-first-cat',
        content: 'Getting Started with Your First Cat

Bringing home your first feline friend is an exciting experience! Here are some essential tips to get you started:

## 1. Prepare Your Home
Before your cat arrives, make sure you have:
- A comfortable bed or sleeping area
- Food and water bowls
- Litter box
- Scratching post
- Some toys for entertainment

## 2. The First Day
When you bring your cat home:
- Let them explore at their own pace
- Show them where the litter box is
- Offer food but do not force them to eat
- Provide a quiet space to rest

## 3. Building Trust
Spend quality time with your new cat:
- Sit near them without forcing interaction
- Speak softly and move slowly
- Offer treats from your hand
- Let them initiate contact when ready

Remember, every cat is unique and will adjust on their own schedule. Be patient and consistent, and you will build a wonderful bond!',
        excerpt: 'Essential tips for new cat owners to build a strong bond with their feline friends.',
        published: true,
        authorId: admin.id,
        categoryId: catCareCategory.id,
        featuredImage: null
      },
      {
        title: 'The Mystery of the Vanishing Treats',
        slug: 'the-mystery-of-the-vanishing-treats',
        content: 'The Mystery of the Vanishing Treats

It was a Tuesday morning when I noticed something strange. The treat bowl, which I had filled just before bed, was completely empty. "Strange," I thought, "I must have forgotten to feed Fluffy."

But then I remembered Fluffy had been sleeping on my pillow, looking completely innocent.

## The Investigation
I decided to play detective and set up a hidden camera to catch the treat thief.

That night, I caught him red-handed, or rather, orange-pawed! It was our dog, Buddy, who had been sneaking treats when no one was looking. The look on Buddy\'s face when he realized he was caught was priceless!

## The Resolution
Instead of scolding Buddy, I came up with a solution. I created a "treat sharing schedule" where Fluffy gets treats at specific times, and Buddy gets a small portion too. Now everyone\'s happy, and the mystery of the vanishing treats has been solved!',
        excerpt: 'A hilarious tale of a dog, a cat, and a treat heist that will make you smile.',
        published: true,
        authorId: admin.id,
        categoryId: catStoriesCategory.id,
        featuredImage: null
      },
      {
        title: 'Cat Care 101: Basic Health Tips',
        slug: 'cat-care-101-basic-health-tips',
        content: 'Cat Care 101: Basic Health Tips

Keeping your cat healthy is one of the most important responsibilities as a pet owner. Here are some fundamental health tips every cat owner should know:

## Regular Vet Checkups
Schedule annual wellness exams even if your cat seems healthy. Early detection of health issues can save lives and money.

## Vaccination Schedule
Keep your cat\'s vaccinations up to date. Core vaccines protect against common feline diseases.

## Dental Health
Dental problems are common in cats. Regular brushing can prevent painful dental issues later in life.

## Nutrition
Feed a balanced diet appropriate for your cat\'s age and activity level. Always provide fresh water.

## Weight Management
Monitor your cat\'s weight and body condition. Obesity can lead to diabetes, joint problems, and other health issues.',
        excerpt: 'Essential health and wellness information for cat owners.',
        published: true,
        authorId: admin.id,
        categoryId: catHealthCategory.id,
        featuredImage: null
      }
    ];

    // Create posts in database
    for (const post of posts) {
      await prisma.post.create({
        data: post
      });
    }

    // Create some gallery images
    const catImages = [
      {
        title: 'Sunbathing Cat',
        description: 'A cat enjoying a nap in the sun',
        imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Sunbathing%20Cat',
        uploaderId: admin.id,
        tags: 'sunny,relaxed'
      },
      {
        title: 'Playful Kitten',
        description: 'A tiny kitten playing with a ball of yarn',
        imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Playful%20Kitten',
        uploaderId: admin.id,
        tags: 'playful,cute,kitten'
      },
      {
        title: 'Elegant Siamese',
        description: 'A beautiful Siamese cat with striking blue eyes',
        imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Elegant%20Siamese',
        uploaderId: admin.id,
        tags: 'elegant,siamese,blue-eyes'
      }
    ];

    for (const image of catImages) {
      await prisma.galleryImage.create({
        data: image
      });
    }

    console.log('Database seeded successfully!');
    console.log('✅ Created admin user: admin@catblog.com');
    console.log('✅ Created 3 regular users: user1@example.com, user2@example.com, user3@example.com');
    console.log('✅ Created 4 sample blog posts');
    console.log('✅ Created 4 sample gallery images');
    console.log('Database is now populated with rich content!');
  } catch (error) {
    console.error('Error seeding database:', error);
  } finally {
    await prisma.$disconnect();
  }
}

seed();

