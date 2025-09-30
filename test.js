        require('dotenv').config(); // Load environment variables

        const sql = require('mssql');

        const config = {
            user: process.env.DB_USER,
            password: process.env.DB_PASSWORD,
            server: process.env.DB_SERVER,
            database: process.env.DB_DATABASE,
            options: {
                encrypt: false, // For Azure SQL Database or if using SSL/TLS
                trustServerCertificate: true // Change to false for production with trusted certificates
            }
        };

        async function testConnection() {
            try {
                await sql.connect(config);
                console.log('Successfully connected to SQL Server!');
            } catch (err) {
                console.error('Database connection failed:', err);
            } finally {
                await sql.close();
            }
        }

        testConnection();