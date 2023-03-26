from requests import post, get
from requests.cookies import RequestsCookieJar
from sys import argv


__SIGNIN_URL = 'https://aisjapan.mlit.go.jp/LoginAction.do'

def getCookies(user_id: str, password: str) -> RequestsCookieJar:
	res = post(__SIGNIN_URL, data={
		'formName': 'ais-web',
		'userID': user_id,
		'password': password
	})
	return res.cookies

class AISJapan:
	__cookies: RequestsCookieJar

	def __init__(self, user_id: str, password: str) -> None:
		self.__cookies = getCookies(user_id, password)
		if self.__cookies is None or 'JSESSIONID' not in self.__cookies:
			raise Exception('Sign In Failed')

	def get(self, url: str) -> str:
		res = get(url, cookies=self.__cookies)
		if res.status_code != 200:
			raise Exception(f'Request Failed (to: {url} , StatusCode: {res.status_code})')
		return res.text

if __name__ == '__main__':
	print(AISJapan(argv[1], argv[2]).get(argv[3]))
