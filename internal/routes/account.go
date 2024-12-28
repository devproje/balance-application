package routes

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"errors"
	"fmt"
	"net/http"

	"github.com/devproje/balance-application/config"
	"github.com/devproje/balance-application/internal/database"
	"github.com/devproje/balance-application/internal/models"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func CreateAccount(ctx *gin.Context) {
	var newAccount models.Account

	if err := ctx.BindJSON(&newAccount); err != nil {
		ctx.JSON(400, gin.H{"error": err.Error()})
		return
	}

	salt, _ := generateRandomSalt()
	hashedPassword, err := hashPassword(newAccount.Password, salt)
	if err != nil {
		ctx.JSON(500, gin.H{"error": "Failed to hash password"})
		return
	}
	newAccount.Password = hashedPassword
	newAccount.Salt = salt

	if err := database.DB.Create(&newAccount).Error; err != nil {
		ctx.JSON(500, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(201, gin.H{"message": "Account created successfully"})
}

func LoginAccount(ctx *gin.Context) {
	var form struct {
		Username string `json:"username"`
		Password string `json:"password"`
	}

	if err := ctx.BindJSON(&form); err != nil {
		ctx.JSON(400, gin.H{"error": err.Error()})
		return
	}

	var account models.Account
	if err := database.DB.Where("username = ?", form.Username).First(&account).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			ctx.JSON(404, gin.H{"error": "Account not found"})
			return
		}
		ctx.JSON(500, gin.H{"error": err.Error()})
		return
	}

	hashedPassword, err := hashPassword(form.Password, account.Salt)
	if err != nil {
		ctx.JSON(500, gin.H{"error": "Failed to hash password"})
		return
	}

	if hashedPassword != account.Password {
		ctx.JSON(401, gin.H{"error": "Invalid credentials"})
		return
	}

	token := generateToken(form.Username, form.Password)
	ctx.JSON(200, gin.H{"message": "Login successful", "token": token})
}

func GetAccount(ctx *gin.Context) {
	var account models.Account
	id := ctx.Param("id")

	if err := database.DB.Where("username = ?", id).First(&account).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			ctx.JSON(404, gin.H{"error": "Account not found"})
			return
		}
		ctx.JSON(500, gin.H{"error": err.Error()})
		return
	}

	account.Password = "hidden"
	account.Salt = "hidden"

	ctx.JSON(http.StatusOK, account)
}

func UpdateAccount(ctx *gin.Context) {
	var updatedAccount models.Account
	id := ctx.Param("id")

	if err := ctx.BindJSON(&updatedAccount); err != nil {
		ctx.JSON(400, gin.H{"error": err.Error()})
		return
	}

	result := database.DB.Model(&models.Account{}).Where("username = ?", id).Updates(updatedAccount)
	if result.Error != nil {
		ctx.JSON(500, gin.H{"error": result.Error.Error()})
		return
	}

	if result.RowsAffected == 0 {
		ctx.JSON(404, gin.H{"error": "Account not found"})
		return
	}

	ctx.JSON(200, gin.H{"message": "Account updated successfully"})
}

func DeleteAccount(ctx *gin.Context) {
	id := ctx.Param("id")

	if err := database.DB.Where("username = ?", id).Delete(&models.Account{}).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			ctx.JSON(404, gin.H{"error": "Account not found"})
			return
		}
		ctx.JSON(500, gin.H{"error": err.Error()})
		return
	}

	ctx.JSON(200, gin.H{"message": "Account deleted successfully"})
}

func hashPassword(password string, salt string) (string, error) {
	salted := fmt.Sprintf("%s:%s", password, salt)
	hash := sha256.Sum256([]byte(salted))

	hashedPassword := hex.EncodeToString(hash[:])
	return hashedPassword, nil
}

func generateRandomSalt() (string, error) {
	salt := make([]byte, config.Get().SaltSize)
	_, err := rand.Read(salt)
	if err != nil {
		return "error", fmt.Errorf("could not generate random salt: %w", err)
	}

	return base64.StdEncoding.EncodeToString(salt), nil
}

func generateToken(username, password string) string {
	combine := fmt.Sprintf("%s:%s", username, password)
	return base64.StdEncoding.EncodeToString([]byte(combine))
}

func VerifyToken(username string, password string) (bool, error) {
	var account models.Account
	if err := database.DB.Where("username = ?", username).First(&account).Error; err != nil {
		if err == gorm.ErrRecordNotFound {
			return false, nil
		}
		return false, err
	}

	hashedPassword, err := hashPassword(password, account.Salt)
	if err != nil {
		return false, err
	}

	if hashedPassword != account.Password {
		return false, nil
	}

	return true, nil
}
