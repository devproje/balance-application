package models

type Account struct {
	Name     string `json:"name" gorm:"column:name"`
	Username string `json:"username" gorm:"primaryKey;column:username"`
	Password string `json:"password" gorm:"column:password"`
	Salt     string `json:"salt" gorm:"column:salt"`
}
