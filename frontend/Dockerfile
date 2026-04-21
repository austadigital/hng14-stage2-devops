# ---- Build ----
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./

RUN npm install --production

COPY . .

# ---- Final ----
FROM node:20-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app .

USER appuser

HEALTHCHECK CMD wget --spider -q http://localhost:3000 || exit 1

CMD ["node", "app.js"]