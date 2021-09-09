$headers = @{}
$headers.Add("Content-Type", "application/json")

$body = '{
    "username": "api-username-goes-here",
    "password": "api-password-goes-here",
    "client_id": "flexvm",
    "grant_type": "password"
}'


$response = Invoke-RestMethod 'https://customerapiauth.fortinet.com/api/v1/oauth/token/' -Method 'POST' -Headers $headers -Body $body
$response | ConvertTo-Json