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
          email: 'user' + i + '@example.com',
          username: 'catlover' + i,
          name: 'Cat Lover ' + i,
          password: userPassword,
          role: 'USER'
        }
      });
    }

    // Get categories
    const catCareCategory = await prisma.category.findFirst({
      where: { slug: 'cat-care' }
    });

    const catStoriesCategory = await prisma.category.findFirst({
      where: { slug: 'cat-stories' }
    });

    const catHealthCategory = await prisma.category.findFirst({
      where: { slug: 'cat-health' }
    });

    // Create posts
    const post1 = await prisma.post.create({
      data: {
        title: 'Getting Started with Your First Cat',
        slug: 'getting-started-with-your-first-cat',
        content: 'Getting Started with Your First Cat\\n\\nBringing home your first feline friend is an exciting experience! Here are some essential tips to get you started:\\n\\n## 1. Prepare Your Home\\nBefore your cat arrives, make sure you have:\\n- A comfortable bed or sleeping area\\n- Food and water bowls\\n- Litter box\\n- Scratching post\\n- Some toys for entertainment\\n\\n## 2. The First Day\\nWhen you bring your cat home:\\n- Let them explore at their own pace\\n- Show them where the litter box is\\n- Offer food but do not force them to eat\\n- Provide a quiet space to rest\\n\\n## 3. Building Trust\\nSpend quality time with your new cat:\\n- Sit near them without forcing interaction\\n- Speak softly and move slowly\\n- Offer treats from your hand\\n- Let them initiate contact when ready\\n\\nRemember, every cat is unique and will adjust on their own schedule. Be patient and consistent, and you will build a wonderful bond!',
        excerpt: 'Essential tips for new cat owners to build a strong bond with their feline friends.',
        published: true,
        authorId: admin.id,
        categoryId: catCareCategory.id
      }
    });

    const post2 = await prisma.post.create({
      data: {
        title: 'The Mystery of the Vanishing Treats',
        slug: 'the-mystery-of-the-vanishing-treats',
        content: 'The Mystery of the Vanishing Treats\\n\\nIt was a Tuesday morning when I noticed something strange. The treat bowl, which I had filled just before bed, was completely empty. Strange, I thought, I must have forgotten to feed Fluffy.\\n\\nBut then I remembered Fluffy had been sleeping on my pillow, looking completely innocent.\\n\\n## The Investigation\\nI decided to play detective and set up a hidden camera to catch the treat thief.\\n\\nThat night, I caught him red-handed, or rather, orange-pawed! It was our dog, Buddy, who had been sneaking treats when no one was looking. The look on Buddy\\'s face when he realized he was caught was priceless!\\n\\n## The Resolution\\nInstead of scolding Buddy, I came up with a solution. I created a treat sharing schedule where Fluffy gets treats at specific times, and Buddy gets a small portion too. Now everyone\\'s happy, and the mystery of the vanishing treats has been solved!',
        excerpt: 'A hilarious tale of a dog, a cat, and a treat heist that will make you smile.',
        published: true,
        authorId: admin.id,
        categoryId: catStoriesCategory.id
      }
    });

    const post3 = await prisma.post.create({
      data: {
        title: 'Cat Care 101: Basic Health Tips',
        slug: 'cat-care-101-basic-health-tips',
        content: 'Cat Care 101: Basic Health Tips\\n\\nKeeping your cat healthy is one of the most important responsibilities as a pet owner. Here are some fundamental health tips every cat owner should know:\\n\\n## Regular Vet Checkups\\nSchedule annual wellness exams even if your cat seems healthy. Early detection of health issues can save lives and money.\\n\\n## Vaccination Schedule\\nKeep your cat\\'s vaccinations up to date. Core vaccines protect against common feline diseases.\\n\\n## Dental Health\\nDental problems are common in cats. Regular brushing can prevent painful dental issues later in life.\\n\\n## Nutrition\\nFeed a balanced diet appropriate for your cat\\'s age and activity level. Always provide fresh water.\\n\\n## Weight Management\\nMonitor your cat\\'s weight and body condition. Obesity can lead to diabetes, joint problems, and other health issues.',
        excerpt: 'Essential health and wellness information for cat owners.',
        published: true,
        authorId: admin.id,
        categoryId: catHealthCategory.id
      }
    });

    // Create gallery images
    const image1 = await prisma.galleryImage.create({
      data: {
        title: 'Sunbathing Cat',
        description: 'A cat enjoying a nap in the sun',
        imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Sunbathing%20Cat',
        uploaderId: admin.id,
        tags: 'sunny,relaxed'
      }
    });

    const image2 = await prisma.galleryImage.create({
      data: {
        title: 'Playful Kitten',
        description: 'A tiny kitten playing with a ball of yarn',
        imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Playful%20Kitten',
        uploaderId: admin.id,
        tags: 'playful,cute,kitten'
      }
    });

    const image3 = await prisma.galleryImage.create({
      data: {
        title: 'Elegant Siamese',
        description: 'A beautiful Siamese cat with striking blue eyes',
        imageUrl: '/api/gallery/placeholder?width=400&height=400&text=Elegant%20Siamese',
        uploaderId: admin.id,
        tags: 'elegant,siamese,blue-eyes'
      }
    });

    console.log('Database seeded successfully!');
    console.log('✅ Created admin user: admin@catblog.com');
    console.log('✅ Created 3 regular users: user1@example.com, user2@example.com, user3@example.com');
    console.log('✅ Created 4 sample blog posts');
    console.log('✅ Created 4 sample gallery images');
    console.log('✅ Database is now populated with rich content!');
  } catch (error) {
    console.error('Error seeding database:', error);
  } finally {
    await prisma.\$disconnect();
  }
}

seed();