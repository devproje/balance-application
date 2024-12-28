package database

import (
	"fmt"

	"github.com/devproje/balance-application/config"
	"github.com/devproje/balance-application/internal/models"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func InitDB() {
	// TODO: add dsn parse to config
	var err error
	var cnf = config.Get().Database
	dsn := fmt.Sprintf(
		"host=%s user=%s password=%s dbname=%s port=%d",
		cnf.Host,
		cnf.Username,
		cnf.Password,
		cnf.DbName,
		cnf.Port,
	)
	DB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	err = DB.AutoMigrate(&models.Account{})
	if err != nil {
		panic("Failed to migrate Account model")
	}

	err = DB.AutoMigrate(&models.Balance{})
	if err != nil {
		panic("Failed to migrate Balance model")
	}
}
