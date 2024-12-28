package main

import (
	"fmt"
	"os"

	"github.com/devproje/balance-application/config"
	"github.com/devproje/balance-application/internal/database"
	"github.com/devproje/balance-application/internal/middleware"
	"github.com/devproje/balance-application/internal/routes"
	"github.com/gin-gonic/gin"
)

func init() {
	var args = os.Args[1:]
	gin.SetMode(gin.ReleaseMode)

	if len(args) > 0 {
		if args[0] == "-d" || args[0] == "--debug" {
			gin.SetMode(gin.DebugMode)
		}
	}
}

func setup(app *gin.Engine) {
	app.Use(middleware.AuthMiddleware())
	api := app.Group("/api")
	{
		auth := api.Group("/account")
		{
			if config.Get().SignUp {
				auth.POST("/signup", routes.CreateAccount)
			}

			auth.POST("/login", routes.LoginAccount)
			auth.GET("/:id", routes.GetAccount)
			auth.PUT("/:id", routes.UpdateAccount)
			auth.DELETE("/:id", routes.DeleteAccount)
		}

		balance := api.Group("/balance")
		{
			balance.POST("/", routes.AddBalance)
			balance.GET("/", routes.GetBalances)
			balance.GET("/:id", routes.GetBalanceByID)
			balance.PUT("/:id", routes.UpdateBalance)
			balance.DELETE("/:id", routes.DeleteBalance)
		}
	}
}

func main() {
	config.InitConfig()
	database.InitDB()
	app := gin.Default()

	setup(app)
	app.Run(fmt.Sprintf(":%d", config.Get().Port))
}
