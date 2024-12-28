package config

import (
	"encoding/json"
	"os"
)

type ConfigData struct {
	Port     int          `json:"port"`
	SignUp   bool         `json:"signup"`
	SaltSize int          `json:"salt_size"`
	Database DatabaseData `json:"db_data"`
}

type DatabaseData struct {
	Host     string `json:"host"`
	Port     int    `json:"port"`
	DbName   string `json:"db_name"`
	Username string `json:"username"`
	Password string `json:"password"`
}

func InitConfig() {
	if _, err := os.ReadFile("config.json"); err != nil {
		ref := ConfigData{
			Port:     8080,
			SaltSize: 10,
			Database: DatabaseData{
				Host:     "localhost",
				Port:     5432,
				DbName:   "balance",
				Username: "user",
				Password: "pass",
			},
		}
		raw, err := json.MarshalIndent(ref, "", "\t")
		if err != nil {
			panic("cannot create config.json file")
		}

		os.WriteFile("config.json", []byte(raw), 0644)
	}
}

func Get() ConfigData {
	var data ConfigData
	raw, err := os.ReadFile("config.json")
	if err != nil {
		panic("cannot read config.json file")
	}

	err = json.Unmarshal(raw, &data)
	if err != nil {
		panic("cannot parse config.json file")
	}

	return data
}
