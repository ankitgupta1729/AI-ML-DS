
const { PrismaClient } = require('@prisma/client');
const bcrypt = require('bcryptjs');
require('dotenv').config();

const prisma = new PrismaClient();

async function main() {
  // Create admin user
  const hashedPassword = await bcrypt.hash('admin123', 12);
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

  console.log('Database seeded successfully!');
  console.log('Admin login: admin@catblog.com / admin123');
}

main().catch(console.error).finally(() => prisma.$disconnect());

