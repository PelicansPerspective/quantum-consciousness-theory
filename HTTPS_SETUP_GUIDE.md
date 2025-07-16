# HTTPS Configuration Checklist for pelicansperspective.com

## 1. Domain DNS Settings
Make sure your domain registrar (where you bought pelicansperspective.com) has these DNS records:

```
Type: CNAME
Name: www
Value: pelicansperspective.github.io

Type: A (for apex domain)
Name: @ (or leave blank)
Value: 185.199.108.153
Value: 185.199.109.153  
Value: 185.199.110.153
Value: 185.199.111.153
```

## 2. GitHub Pages Settings
1. Go to your repository: https://github.com/PelicansPerspective/quantum-consciousness-theory
2. Click "Settings" tab
3. Scroll down to "Pages" section
4. Make sure:
   - Source: "Deploy from a branch"
   - Branch: "main"
   - Folder: "/docs"
   - Custom domain: "pelicansperspective.com"
   - ✅ "Enforce HTTPS" should be CHECKED

## 3. Wait for SSL Certificate
- After updating DNS, GitHub Pages automatically provisions an SSL certificate
- This can take 24-48 hours to fully propagate
- You can check status in GitHub Pages settings

## 4. Common Issues & Solutions

### If you see "Site not secure":
1. **DNS Propagation**: Use https://www.whatsmydns.net/ to check if your DNS has propagated globally
2. **Mixed Content**: All resources must use HTTPS (we've already fixed this)
3. **Certificate Provisioning**: GitHub may still be generating your SSL certificate

### Force HTTPS:
- The security headers we added will help force HTTPS
- GitHub Pages should automatically redirect HTTP to HTTPS once SSL is active

## 5. Testing Steps
1. Wait 24-48 hours after DNS changes
2. Try accessing: https://pelicansperspective.com
3. Check certificate in browser (click lock icon)
4. Test redirect: http://pelicansperspective.com should redirect to HTTPS

## 6. Immediate Actions Needed
1. ✅ Update DNS records at your domain registrar
2. ✅ Enable "Enforce HTTPS" in GitHub Pages settings
3. ⏳ Wait for SSL certificate provisioning (automatic)

The website code is now fully secure and ready for HTTPS!
