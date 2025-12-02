# Streamlit App Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. Data Preparation
- [ ] Trained models exist in `model_outputs/trained_models.pkl`
- [ ] Evaluation results exist in `model_outputs/final_evaluation_results.json`
- [ ] Train matrix exists in `model_outputs/train_matrix.npz`
- [ ] Mappings exist in `features/mappings.pkl`
- [ ] Game popularity exists in `features/game_popularity.csv`

### 2. Pre-compute Recommendations
```bash
cd streamlit_app
python precompute_recommendations.py
```
- [ ] Script runs without errors
- [ ] File `model_outputs/all_user_recommendations.json` is created
- [ ] File size is reasonable (< 100MB for free deployment)
- [ ] JSON is valid and contains expected data

### 3. Test Locally
```bash
pip install streamlit plotly
streamlit run app.py
```
- [ ] App loads without errors
- [ ] Home page displays correctly
- [ ] User Recommendations page works
- [ ] Model Explorer page renders
- [ ] About page loads
- [ ] Navigation works between pages
- [ ] Charts are interactive
- [ ] Game cards display (with images or placeholders)
- [ ] User search functionality works

### 4. Check File Sizes
```bash
du -sh model_outputs/all_user_recommendations.json
du -sh model_outputs/trained_models.pkl
```
- [ ] Recommendations JSON < 100MB (for GitHub)
- [ ] If larger, reduce MAX_USERS in precompute script
- [ ] Total repo size < 1GB

### 5. Dependencies
- [ ] `requirements.txt` is complete
- [ ] All imports work
- [ ] No missing packages

## 🚀 Deployment Options

### Option 1: Streamlit Community Cloud (Recommended)

**Pros:** Free, easy, automatic updates
**Cons:** Public only, limited resources

**Steps:**
1. [ ] Create GitHub repository
2. [ ] Push code to GitHub
   ```bash
   git add streamlit_app/
   git commit -m "Add Streamlit app"
   git push
   ```
3. [ ] Go to https://share.streamlit.io
4. [ ] Connect GitHub account
5. [ ] Select repository and `streamlit_app/app.py`
6. [ ] Deploy!

**Important:**
- [ ] Ensure all paths are relative
- [ ] Include all necessary files
- [ ] Check file sizes (< 100MB per file)
- [ ] Test with sample data first

### Option 2: Local Server

**Pros:** Full control, private
**Cons:** Requires server setup

**Steps:**
1. [ ] Set up virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
2. [ ] Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. [ ] Run app
   ```bash
   streamlit run app.py --server.port 8501
   ```
4. [ ] (Optional) Set up systemd service for auto-start

### Option 3: Docker Container

**Pros:** Portable, reproducible
**Cons:** Requires Docker knowledge

**Dockerfile:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**Steps:**
1. [ ] Create Dockerfile
2. [ ] Build image: `docker build -t playnext-app .`
3. [ ] Run container: `docker run -p 8501:8501 playnext-app`

## 🔍 Pre-Launch Testing

### Functionality Tests
- [ ] Load home page → Check metrics display
- [ ] Navigate to User Recommendations → Search for user
- [ ] View user recommendations → Check game cards
- [ ] Check bundle completion suggestions
- [ ] Navigate to Model Explorer → Verify tabs work
- [ ] Navigate to About → Ensure all content loads
- [ ] Test on different browsers (Chrome, Firefox, Safari)
- [ ] Test on mobile device (responsive design)

### Performance Tests
- [ ] Initial load time < 5 seconds
- [ ] Page navigation < 1 second
- [ ] User search is responsive
- [ ] Charts are interactive
- [ ] No console errors
- [ ] No memory leaks (check browser dev tools)

### Data Validation
- [ ] Metrics match evaluation results
- [ ] User recommendations are personalized
- [ ] Game IDs are correct
- [ ] Scores are in expected ranges
- [ ] Bundle ownership percentages make sense

## 🐛 Troubleshooting

### Issue: Import errors
**Fix:** 
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Models not found"
**Fix:** 
- Check path in `utils.py`
- Ensure models are in correct location
- Use relative paths, not absolute

### Issue: Slow loading
**Fix:**
- Pre-compute more recommendations
- Reduce MAX_USERS
- Check caching decorators (@st.cache_data)
- Use faster hardware

### Issue: Large file size
**Fix:**
- Reduce MAX_USERS in `precompute_recommendations.py`
- Reduce K_RECOMMENDATIONS
- Use Git LFS for large files
- Consider external data storage

### Issue: Images not loading
**Fix:**
- Check Steam CDN availability
- Verify app IDs are extracted correctly
- Fallback placeholders should work automatically
- Check browser console for errors

## 📊 Post-Deployment

### Monitor
- [ ] Check app logs for errors
- [ ] Monitor memory usage
- [ ] Track page load times
- [ ] Gather user feedback

### Optimize
- [ ] Profile slow pages
- [ ] Add more caching if needed
- [ ] Compress images
- [ ] Lazy load content

### Update
- [ ] Keep dependencies up to date
- [ ] Add new features based on feedback
- [ ] Improve visualizations
- [ ] Enhance documentation

## 🎉 Success Indicators

Your deployment is successful if:
- ✅ App is accessible via URL
- ✅ All pages load without errors
- ✅ Recommendations are displayed correctly
- ✅ Charts are interactive
- ✅ Theme looks good
- ✅ Performance is acceptable (< 5s load)
- ✅ No critical errors in logs
- ✅ Users can navigate easily

## 📝 Deployment Notes

**Date deployed:** _____________

**Deployment platform:** 
- [ ] Streamlit Cloud
- [ ] Local server
- [ ] Docker
- [ ] Other: ___________

**URL:** _____________

**Number of users:** _____________

**File sizes:**
- Recommendations JSON: _______ MB
- Total repo size: _______ MB

**Performance:**
- Load time: _______ seconds
- Memory usage: _______ MB

**Issues encountered:** _____________

**Resolved:** _____________

---

## 🚀 Ready to Deploy?

Once all boxes are checked, you're ready to share your app with the world!

**Quick deploy command:**
```bash
cd streamlit_app
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Good luck! 🎮
