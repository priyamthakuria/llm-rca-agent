# Documentation Index

Welcome to the LLM-RCA-Agent documentation! This folder contains all setup and learning guides.

## 📖 Available Guides

### Setup Guides

1. **`FIX_PYTHON_NOT_SHOWING.md`** ⭐ **START HERE IF PYTHON NOT SHOWING**
   - **Specific fix for Python version not appearing in bottom-right**
   - Step-by-step solution
   - Most common issue - install Python plugin!

2. **`INTELLIJ_SETUP.md`** ⭐ **COMPLETE SETUP GUIDE**
   - Complete guide for setting up IntelliJ IDEA
   - All methods explained
   - Comprehensive troubleshooting
   - Use this for full setup instructions

3. **`QUICK_START.md`**
   - 5-minute quick start guide
   - Essential steps to get running
   - Quick troubleshooting tips

### Learning Guides

4. **`LEARNING_GUIDE.md`**
   - Complete tutorial explaining the entire project
   - Assumes only Python knowledge
   - Explains every concept from scratch
   - Deep dive into each component
   - **Read this to understand everything!**

### Project Documentation

4. **`../README.md`** (in project root)
   - Project overview
   - Structure explanation
   - Usage examples

5. **`../data/README.md`** (in data folder)
   - Data schema explanation
   - Incident format documentation

---

## 🎯 Which Guide Should I Read?

### "Python version is NOT showing in IntelliJ bottom-right" ⚠️
→ Read **`FIX_PYTHON_NOT_SHOWING.md`** (Most common issue!)

### "I can't set up IntelliJ IDEA"
→ Read **`INTELLIJ_SETUP.md`**

### "I want to understand the project"
→ Read **`LEARNING_GUIDE.md`**

### "I just want to run it quickly"
→ Read **`QUICK_START.md`**

### "I want project overview"
→ Read **`../README.md`** (in project root)

---

## 🔧 Common Issues

### Python Version Not Showing in IntelliJ
**Solution:** See **`FIX_PYTHON_NOT_SHOWING.md`** - This is the dedicated guide for this issue!

### Import Errors
**Solution:** See `INTELLIJ_SETUP.md` → Step 3: Mark Source Directories

### Packages Not Found
**Solution:** 
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "No module named 'src'"
**Solution:** Mark `src` as Sources Root (see `INTELLIJ_SETUP.md`)

---

## 📝 Quick Reference

**Virtual Environment Path:**
```
/Users/priyamthakuria/Desktop/dev/llm-rca-agent/venv/bin/python
```

**Project Root:**
```
/Users/priyamthakuria/Desktop/dev/llm-rca-agent
```

**Key Commands:**
```bash
# Activate venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate data
python -m src.data.generator --num_incidents 300

# Run experiment
python -m src.experiments.runner --config experiments/configs/exp_zero_shot.yaml
```

---

## 🆘 Need Help?

1. Check the relevant guide above
2. See troubleshooting sections in each guide
3. Verify your setup matches the checklist in `INTELLIJ_SETUP.md`

---

## 📚 Learning Path

**For Beginners:**
1. Read `QUICK_START.md` to get running
2. Read `../LEARNING_GUIDE.md` to understand everything
3. Experiment with the code

**For Experienced Developers:**
1. Read `../README.md` for overview
2. Check `INTELLIJ_SETUP.md` for IDE setup
3. Explore the codebase

