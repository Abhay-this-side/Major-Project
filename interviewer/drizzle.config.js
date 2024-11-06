/** @type { import("drizzle-kit").Config } */
export default {
    schema: "./utils/schema.js",
    dialect: 'postgresql',
    dbCredentials: {
      url:'postgresql://neondb_owner:9BJg6YMnUDVo@ep-icy-leaf-a5f9mil5.us-east-2.aws.neon.tech/Interviewer?sslmode=require',
    }
  };
  