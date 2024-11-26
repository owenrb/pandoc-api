# pandoc-api

File converter API via [Pandoc](https://pandoc.org/)

### Run image from Docker Hub

1. **Pull Docker image**:

   ```sh
   docker pull owenrbee/pandoc-api:1.0
   ```

2. **Run the Docker container**:

   ```sh
   docker run --rm -p 5050:5050 owenrbee/pandoc-api:1.0
   ```

### Build and Run the Docker Container

1. **Build the Docker image**:

   ```sh
   docker build -t owenrbee/pandoc-api .
   ```

2. **Run the Docker container**:

   ```sh
   docker run --rm -p 5050:5050 owenrbee/pandoc-api
   ```

3. **Access Swagger UI** (http://localhost:5050/swagger):
   You can now access the API documentation and test the conversion service using tools like `curl` or Postman.
