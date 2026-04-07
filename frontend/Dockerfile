FROM node:18-alpine

WORKDIR /app

# Copy dependency files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy full source
COPY . .

# Build the dynamic Next.js application
RUN npm run build

EXPOSE 3000

ENV PORT=3000
# Run the Next.js server locally
CMD ["npm", "start"]
