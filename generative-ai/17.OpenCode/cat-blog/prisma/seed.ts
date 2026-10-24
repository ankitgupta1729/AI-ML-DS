import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'
import 'dotenv/config'

const prisma = new PrismaClient()

async function main() {
  // Create admin user
  const hashedPassword = await bcrypt.hash('admin123', 12)
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
  })

  // Create regular user
  const userPassword = await bcrypt.hash('user123', 12)
  const user = await prisma.user.upsert({
    where: { email: 'user@catblog.com' },
    update: {},
    create: {
      email: 'user@catblog.com',
      username: 'catlover',
      name: 'Cat Lover',
      password: userPassword,
      role: 'USER'
    }
  })

  // Create categories
  const catCareCategory = await prisma.category.upsert({
    where: { slug: 'cat-care' },
    update: {},
    create: {
      name: 'Cat Care',
      slug: 'cat-care',
      description: 'Tips and advice for taking care of your feline friends',
      color: '#10b981'
    }
  })

  const storiesCategory = await prisma.category.upsert({
    where: { slug: 'cat-stories' },
    update: {},
    create: {
      name: 'Cat Stories',
      slug: 'cat-stories',
      description: 'Heartwarming and funny stories about cats',
      color: '#f59e0b'
    }
  })

  const healthCategory = await prisma.category.upsert({
    where: { slug: 'cat-health' },
    update: {},
    create: {
      name: 'Cat Health',
      slug: 'cat-health',
      description: 'Health and wellness information for cats',
      color: '#ef4444'
    }
  })

  // Create tags
  const cuteTag = await prisma.tag.upsert({
    where: { slug: 'cute' },
    update: {},
    create: {
      name: 'cute',
      slug: 'cute',
      color: '#ec4899'
    }
  })

  const funnyTag = await prisma.tag.upsert({
    where: { slug: 'funny' },
    update: {},
    create: {
      name: 'funny',
      slug: 'funny',
      color: '#8b5cf6'
    }
  })

  // Create sample posts
  const post1 = await prisma.post.create({
    data: {
      title: '10 Essential Tips for New Cat Owners',
      slug: '10-essential-tips-for-new-cat-owners',
      content: `# 10 Essential Tips for New Cat Owners

Congratulations on your new feline friend! Here are the most important things you need to know:

## 1. Create a Safe Space
Your cat needs a quiet place to retreat to when feeling overwhelmed. This could be a spare room or even just a cozy corner with a bed.

## 2. Provide Proper Nutrition
Choose high-quality cat food appropriate for your cat's age and health needs. Always provide fresh water.

## 3. Regular Vet Checkups
Schedule regular veterinary visits to keep your cat healthy and up-to-date on vaccinations.

## 4. Litter Box Management
Keep the litter box clean and in a quiet, accessible location. A good rule is one box per cat plus one extra.

## 5. Play and Exercise
Cats need mental and physical stimulation. Use interactive toys and play with your cat daily.

## 6. Grooming
Regular brushing helps reduce shedding and prevents hairballs.

## 7. Scratching Posts
Provide appropriate scratching surfaces to save your furniture.

## 8. Microchip and ID
Ensure your cat has proper identification in case they get lost.

## 9. Understanding Cat Behavior
Learn to read your cat's body language and vocalizations.

## 10. Patience and Love
Building trust takes time, but the reward is a loving companion for years to come.`,
      excerpt: 'Essential guidance for new cat parents to ensure a happy, healthy relationship with their feline companion.',
      published: true,
      authorId: admin.id,
      categoryId: catCareCategory.id,
      tags: {
        connect: [{ id: cuteTag.id }]
      }
    }
  })

  const post2 = await prisma.post.create({
    data: {
      title: 'The Mysterious Case of the Vanishing Cat Food',
      slug: 'the-mysterious-case-of-the-vanishing-cat-food',
      content: `# The Mysterious Case of the Vanishing Cat Food

It was a Tuesday morning when I noticed something strange. The cat food bowl, which I had filled just before bed, was completely empty. But my cat, Whiskers, was fast asleep on the couch, looking innocent as can be.

## The Investigation Begins

I checked the security cameras, expecting to see Whiskers having a midnight feast. But what I found was much more surprising...

*Camera footage shows Whiskers leading a raid of neighborhood cats*
*They work in perfect coordination, taking turns distracting the dog while others feast*

## The Conspiracy Deepens

After weeks of observation, I discovered this wasn't just about food. These cats had organized a sophisticated operation with:
- Lookouts posted at windows
- Distraction tactics involving the neighbor's dog  
- An elaborate communication system using meows and tail signals
- A shared food stash in the garage

## The Resolution

Rather than putting an end to their operation, I decided to embrace it. Now I leave extra food out and watch the nightly cat meetings from my window. Sometimes the best solutions come from understanding rather than controlling nature.

Whiskers just gives me that knowing look that says, "You finally figured it out, didn't you, human?"`,
      excerpt: 'A hilarious tale of discovering your cat is the mastermind of a neighborhood food conspiracy.',
      published: true,
      authorId: user.id,
      categoryId: storiesCategory.id,
      tags: {
        connect: [{ id: funnyTag.id }]
      }
    }
  })

  console.log('Database seeded successfully!')
  console.log('Admin login: admin@catblog.com / admin123')
  console.log('User login: user@catblog.com / user123')
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })