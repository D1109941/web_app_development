document.addEventListener("DOMContentLoaded", function() {
    // Dynamic ingredients logic for new/edit
    const addIngBtn = document.getElementById('addIngredientRow');
    if (addIngBtn) {
        addIngBtn.addEventListener('click', function() {
            const container = document.getElementById('ingredientsContainer');
            const rowFragment = document.createElement('div');
            rowFragment.className = 'row g-3 mb-2 row-ingredient fade-in align-items-center';
            rowFragment.innerHTML = `
                <div class="col-6">
                    <input type="text" class="form-control" name="ingredient_name[]" placeholder="食材名稱 (例: 牛肉)" required>
                </div>
                <div class="col-4">
                    <input type="text" class="form-control" name="ingredient_amount[]" placeholder="份量 (例: 300g)" required>
                </div>
                <div class="col-2 text-end">
                    <button type="button" class="btn btn-outline-danger btn-sm rounded-circle px-2 remove-ing-btn border-0"><i class="fa-solid fa-xmark"></i></button>
                </div>
            `;
            container.appendChild(rowFragment);
        });

        document.getElementById('ingredientsContainer').addEventListener('click', function(e) {
            if (e.target.closest('.remove-ing-btn')) {
                e.target.closest('.row-ingredient').remove();
            }
        });
    }

    // Timer Logic
    const startBtn = document.getElementById('btnStartTimer');
    let timerInterval;

    if (startBtn) {
        startBtn.addEventListener('click', function() {
            const minInput = document.getElementById('timerMinutes').value;
            const display = document.getElementById('timerDisplay');
            
            if (!minInput || minInput <= 0) return;
            
            let totalSeconds = parseInt(minInput) * 60;
            clearInterval(timerInterval);
            
            startBtn.disabled = true;
            
            timerInterval = setInterval(() => {
                totalSeconds--;
                let m = Math.floor(totalSeconds / 60);
                let s = totalSeconds % 60;
                display.innerText = `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
                
                if (totalSeconds <= 0) {
                    clearInterval(timerInterval);
                    display.innerText = "完成！";
                    startBtn.disabled = false;
                    alert("烹飪時間到！趕快去看看你的料理吧！\u23f0");
                }
            }, 1000);
        });
    }

    // Checklist Toggle via AJAX
    const checklistChecks = document.querySelectorAll('.checklist-toggle');
    checklistChecks.forEach(check => {
        check.addEventListener('change', function() {
            const itemId = this.dataset.id;
            const label = this.nextElementSibling;
            
            fetch(`/collection/checklist/${itemId}/toggle`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                }
            }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    label.style.textDecoration = this.checked ? 'line-through' : 'none';
                    label.style.opacity = this.checked ? '0.5' : '1';
                } else {
                    this.checked = !this.checked; 
                }
            }).catch(e => {
                console.error("Error toggling:", e);
                this.checked = !this.checked;
            });
        });
    });
});
