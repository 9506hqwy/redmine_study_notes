# 認証と認可

## OAuth2

Redmine 6.1 で OAuth2 対応した。

PKCE は必要ない。

### アプリケーション登録

1. [管理]-[設定]-[API] で [RESTによるWebサービスを有効にする] を有効化する。
2. [管理]-[アプリケーション] で [新しいアプリケーション] を作成する。
   - コールバック URL は urn:ietf:wg:oauth:2.0:oob を設定するとブラウザに認可コードを表示できる。
3. アプリケーション ID とシークレットが発行される。

### 利用

生成されたアプリケーション ID とシークレットは下記とする。

```text
アプリケーションID: 76iEUCf88ynVSsIVHxP06LBGSoSAeAfXhTBGLgkEX6E
シークレット: mGu2o9fry7b56ZPZBcwfyWq7OZYcKgdXMMiOFiDULWo
```

認可コードを要求する URL を生成する。

```sh
AUTHZ_TYPE=code
CLIENT_ID=76iEUCf88ynVSsIVHxP06LBGSoSAeAfXhTBGLgkEX6E
REDIRECT_URI=urn:ietf:wg:oauth:2.0:oob
STATE=abc
SITE_URL=http://127.0.0.1:3000/oauth/authorize

echo "${SITE_URL}?response_type=${AUTHZ_TYPE}&client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&state=${STATE}"
```

```text
http://127.0.0.1:3000/oauth/authorize?response_type=code&client_id=76iEUCf88ynVSsIVHxP06LBGSoSAeAfXhTBGLgkEX6E&redirect_uri=urn:ietf:wg:oauth:2.0:oob&state=abc
```

ブラウザで上記の URL に接続しアプリケーションを承認すると認可コードが生成される。

```text
認可コード: vL1o0GYxsN1QZBNyTiRb5EI2WLYABx9aa7KVfBLrme4
```

アクセストークンを要求する。

```sh
GRANT_TYPE=authorization_code
CLIENT_SECRET=mGu2o9fry7b56ZPZBcwfyWq7OZYcKgdXMMiOFiDULWo
REDIRECT_URI=urn:ietf:wg:oauth:2.0:oob
CODE=vL1o0GYxsN1QZBNyTiRb5EI2WLYABx9aa7KVfBLrme4
SITE_URL=http://127.0.0.1:3000/oauth/token

curl -sS \
    -u "${CLIENT_ID}:${CLIENT_SECRET}" \
    -X POST \
    -d "grant_type=${GRANT_TYPE}" \
    -d "redirect_uri=${REDIRECT_URI}" \
    -d "code=${CODE}" \
    "${SITE_URL}" | jq
```

```json
{
  "access_token": "XjgptuJ9CPfv-bkeZmqAVoZK0CMOwbUyqTLT22_8NtY",
  "token_type": "Bearer",
  "expires_in": 7200,
  "refresh_token": "MMZi3Fn01LKNYr3XTlcYn2GBseA1bheGdjV75stZk7s",
  "scope": "view_project search_project view_members",
  "created_at": 1772335837
}
```

非公開プロジェクトの場合は承認したユーザがプロジェクトのメンバになっている必要がある。

```sh
curl -H "Authorization: Bearer XjgptuJ9CPfv-bkeZmqAVoZK0CMOwbUyqTLT22_8NtY" http://127.0.0.1:3000/projects.json | jq
```

```json
{
  "projects": [
    {
      "id": 1,
      "name": "テストプロジェクト",
      "identifier": "test-project",
      "description": "",
      "homepage": "",
      "status": 1,
      "is_public": false,
      "inherit_members": false,
      "created_on": "2026-02-26T10:52:11Z",
      "updated_on": "2026-03-01T03:00:11Z"
    }
  ],
  "total_count": 1,
  "offset": 0,
  "limit": 25
}
```

## 参考

- [OAuth2 support for Redmine API Apps (OAuth2 Provider)](https://www.redmine.org/issues/24808)
- [doorkeeper](https://github.com/doorkeeper-gem/doorkeeper)
