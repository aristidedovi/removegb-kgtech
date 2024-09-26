# Use the official Node.js 20 image as the base for the build stage

FROM node:20-alpine as builder

# Set the working directory

WORKDIR /app

# Copy package.json and package-lock.json

COPY package*.json ./

# Increase the timeout for npm

RUN npm config set fetch-retry-maxtimeout 60000

# Use a different npm registry (optional)

RUN npm config set registry https://registry.npmjs.org/

# Update npm to the latest version

RUN npm install -g npm@latest

# Install dependencies

RUN npm install

# Correctly copy the entire project

COPY . .

# Set environment variables
ARG NEXT_PUBLIC_FLASK_PUBLIC_API_URL
ARG NEXT_PUBLIC_FLASK_PUBLIC_URL
ENV NEXT_PUBLIC_FLASK_PUBLIC_API_URL=http://localhost:5000/api/v1
ENV NEXT_PUBLIC_FLASK_PUBLIC_URL=http://localhost:5000

# Build the Next.js app

#RUN npm run build --skip-nx-cache
RUN npm run build

# After the npm run build step

RUN ls -la /app/.next

# Use the official Node.js 20 image as the base for the production stage

FROM builder as production

# Set the working directory
WORKDIR /app

#FLASK_PUBLIC_API_URL: http://backend:5000/api/v1
#FLASK_PUBLIC_URL: http://backend:5000/

# Install production dependencies
RUN npm install --production

# Copy the entire app from the builder stage

#COPY --from=builder /app .
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public



# Expose the port the app will run on
EXPOSE 3000


# Start the app

CMD ["npm", "start"]