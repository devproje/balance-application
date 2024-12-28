package routes

import (
	"github.com/devproje/balance-application/internal/database"
	"github.com/devproje/balance-application/internal/models"
	"github.com/gin-gonic/gin"
)

func AddBalance(ctx *gin.Context) {
	var balance models.Balance

	if err := ctx.ShouldBindJSON(&balance); err != nil {
		ctx.JSON(400, gin.H{"error": err.Error()})
		return
	}

	if err := database.DB.Create(&balance).Error; err != nil {
		ctx.JSON(500, gin.H{"error": "Failed to create balance"})
		return
	}

	ctx.JSON(201, balance)
}

func GetBalances(ctx *gin.Context) {
	var balances []models.Balance
	if err := database.DB.Find(&balances).Error; err != nil {
		ctx.JSON(500, gin.H{"error": "Failed to retrieve balances"})
		return
	}
	ctx.JSON(200, balances)
}

func GetBalanceByID(ctx *gin.Context) {
	id := ctx.Param("id")
	var balance models.Balance

	if err := database.DB.Where("id = ?", id).First(&balance).Error; err != nil {
		ctx.JSON(404, gin.H{"error": "Balance not found"})
		return
	}

	ctx.JSON(200, balance)
}

func UpdateBalance(ctx *gin.Context) {
	id := ctx.Param("id")
	var balance models.Balance

	if err := database.DB.Where("id = ?", id).First(&balance).Error; err != nil {
		ctx.JSON(404, gin.H{"error": "Balance not found"})
		return
	}

	if err := ctx.ShouldBindJSON(&balance); err != nil {
		ctx.JSON(400, gin.H{"error": err.Error()})
		return
	}

	if err := database.DB.Save(&balance).Error; err != nil {
		ctx.JSON(500, gin.H{"error": "Failed to update balance"})
		return
	}

	ctx.JSON(200, balance)
}

func DeleteBalance(ctx *gin.Context) {
	id := ctx.Param("id")
	var balance models.Balance

	if err := database.DB.Where("id = ?", id).First(&balance).Error; err != nil {
		ctx.JSON(404, gin.H{"error": "Balance not found"})
		return
	}

	if err := database.DB.Where("id = ?", id).Delete(&balance).Error; err != nil {
		ctx.JSON(500, gin.H{"error": "Failed to delete balance"})
		return
	}

	ctx.JSON(200, gin.H{"message": "Balance deleted successfully"})
}
