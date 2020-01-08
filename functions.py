def checkLogin(jsonData, email, password):
	for user in jsonData:
		if email == user.email
			if checkPass(user.password, password)
				return True
	return False

def checkPass(passSaved, passIn):
    if passSaved == passIn:
        return True
    return False
