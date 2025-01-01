package models

type Balance struct {
	ID      uint    `json:"id" gorm:"primaryKey;column:id"`
	UID     string  `json:"uid" gorm:"column:uid"`
	Name    string  `json:"name" gorm:"column:name"`
	Date    int64   `json:"date" gorm:"column:date"`
	Price   int64   `json:"price" gorm:"column:price"`
	Buy     bool    `json:"buy" gorm:"column:buy"`
	Memo    string  `json:"memo" gorm:"column:memo"`
	Account Account `json:"-" gorm:"foreignKey:UID;references:Username;constraint:FK_Account_ID;onUpdate:CASCADE;onDelete:CASCADE"`
}
