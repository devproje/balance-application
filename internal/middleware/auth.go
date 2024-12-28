package middleware

import (
	"encoding/base64"
	"strings"

	"github.com/devproje/balance-application/internal/routes"
	"github.com/gin-gonic/gin"
)

func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		excludedPaths := []string{"/", "/api/account/login", "/api/account/signup"}
		for _, path := range excludedPaths {
			if strings.HasPrefix(c.Request.URL.Path, path) {
				c.Next()
				return
			}
		}

		authHeader := c.GetHeader("Authorization")
		if authHeader == "" {
			c.JSON(401, gin.H{"error": "Missing Authorization header"})
			c.Abort()
			return
		}

		parts := strings.Split(authHeader, " ")
		if len(parts) != 2 || parts[0] != "Basic" {
			c.JSON(401, gin.H{"error": "Invalid Authorization header format"})
			c.Abort()
			return
		}

		credentials, err := base64.StdEncoding.DecodeString(parts[1])
		if err != nil {
			c.JSON(401, gin.H{"error": "Failed to decode credentials"})
			c.Abort()
			return
		}

		idx := strings.IndexByte(string(credentials), ':')
		if idx == -1 {
			c.JSON(401, gin.H{"error": "Invalid credentials format"})
			c.Abort()
			return
		}
		username := string(credentials[:idx])
		password := string(credentials[idx+1:])

		isValid, err := routes.VerifyToken(username, password)
		if err != nil {
			c.JSON(500, gin.H{"error": err.Error()})
			c.Abort()
			return
		}

		if !isValid {
			c.JSON(401, gin.H{"error": "Invalid credentials"})
			c.Abort()
			return
		}

		c.Next()
	}
}
