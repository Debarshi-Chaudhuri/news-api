FROM amazoncorretto:11

# Set working directory
WORKDIR /home/dynamodblocal

# Install required packages
RUN yum install -y wget tar gzip

# Download DynamoDB Local
RUN wget https://d1ni2b6xgvw0s0.cloudfront.net/v2.0/dynamodb_local_latest.tar.gz -O dynamodb_local_latest.tar.gz && \
    tar -xzf dynamodb_local_latest.tar.gz && \
    rm dynamodb_local_latest.tar.gz

# Create a non-root user to run DynamoDB
RUN groupadd -r dynamodb && \
    useradd -r -g dynamodb dynamodb && \
    chown -R dynamodb:dynamodb /home/dynamodblocal

# Switch to non-root user
USER dynamodb

# Set up volume for persistent data
VOLUME ["/home/dynamodblocal/data"]

# Expose DynamoDB port
EXPOSE 9000

# Command to run DynamoDB Local
CMD ["java", "-jar", "DynamoDBLocal.jar", "-sharedDb", "-dbPath", "/home/dynamodblocal/data"]