package main

import (
	"fmt"
	"os"

	"github.com/devproje/balance-application/config"
	"github.com/devproje/balance-application/internal/database"
	"github.com/devproje/balance-application/internal/middleware"
	"github.com/devproje/balance-application/internal/routes"
	"github.com/devproje/plog/level"
	"github.com/devproje/plog/log"
	"github.com/gin-gonic/gin"
)

func check(target string, args []string) bool {
	for i := 0; i < len(args); i++ {
		if args[i] == target {
			return true
		}
	}

	return false
}

func init() {
	var args = os.Args[1:]
	gin.SetMode(gin.ReleaseMode)
	log.SetLevel(level.Info)

	if len(args) > 0 {
		if check("-d", args) || check("--debug", args) {
			gin.SetMode(gin.DebugMode)
			log.SetLevel(level.Trace)
		}

		if check("--create-sample", args) || check("-sa", args) {
			err := config.CreateSample()
			if err != nil {
				panic(err)
			}

			return
		}
	}
}

func setup(app *gin.Engine) {
	app.Use(middleware.CORS)
	app.Use(middleware.AuthMiddleware())

	app.GET("/", func(ctx *gin.Context) {
		ctx.String(200, "service is healty")
	})
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
	log.Infof("server port bind at: %d", config.Get().Port)

	app.Run(fmt.Sprintf(":%d", config.Get().Port))
}
