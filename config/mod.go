package config

import (
	"encoding/json"
	"os"
)

type ConfigData struct {
	Port       int          `json:"port"`
	SignUp     bool         `json:"signup"`
	SaltSize   int          `json:"salt_size"`
	CorsOrigin string       `json:"cors_origin"`
	Database   DatabaseData `json:"db_data"`
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
		raw := createRaw()
		os.WriteFile("config.json", raw, 0644)
	}
}

func CreateSample() error {
	if _, err := os.ReadFile("config.sample.json"); err != nil {
		_, err = os.Create("config.sample.json")
		if err != nil {
			return err
		}
	}

	err := os.WriteFile("config.sample.json", createRaw(), 0644)
	if err != nil {
		return err
	}

	return nil
}

func createRaw() []byte {
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

	return raw
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
