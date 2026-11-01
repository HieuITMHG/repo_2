import express, { Request, Response } from "express";

const app = express();
app.use(express.json());

/**
 * LEVEL 2 (MEDIUM): Express :userId param
 * Route: GET /api/v1/users/:userId/status
 * Matches repo_1 UserClient.getUserStatus(userId)
 */
app.get("/api/v1/users/:userId/status", (req: Request, res: Response) => {
  const { userId } = req.params;
  res.status(200).json({
    userId,
    active: true,
    tier: "PREMIUM",
    lastLogin: new Date().toISOString()
  });
});

export default app;
