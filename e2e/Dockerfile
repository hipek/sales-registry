FROM mcr.microsoft.com/playwright:v1.56.1-jammy AS base

WORKDIR /app

COPY e2e/package.json e2e/pnpm-lock.yaml ./
RUN corepack enable && corepack prepare pnpm@9 --activate && pnpm install --frozen-lockfile

COPY e2e/ .

CMD ["pnpm", "test"]
