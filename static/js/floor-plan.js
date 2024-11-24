class FloorPlan {
    constructor(containerId, tables, options = {}) {
        this.container = document.getElementById(containerId);
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.tables = tables;
        this.selectedTable = null;
        this.hoveredTable = null;
        this.isAdmin = options.isAdmin || false;
        this.onTableSelect = options.onTableSelect || (() => {});
        
        // Configuration
        this.config = {
            gridSize: 50,
            tableWidth: 60,
            tableHeight: 60,
            roundTableRadius: 30,
            padding: 20,
            colors: {
                available: '#28a745',
                reserved: '#dc3545',
                vip: '#d4af37',
                selected: '#007bff',
                hovered: '#17a2b8',
                text: '#ffffff'
            }
        };
        
        // Setup
        this.container.appendChild(this.canvas);
        this.setupEventListeners();
        this.resize();
        this.render();
        
        // Add resize listener
        window.addEventListener('resize', () => {
            this.resize();
            this.render();
        });
    }
    
    resize() {
        const rect = this.container.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
        this.scale = Math.min(
            (rect.width - this.config.padding * 2) / 600,
            (rect.height - this.config.padding * 2) / 450
        );
    }
    
    setupEventListeners() {
        this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
        this.canvas.addEventListener('mouseleave', () => {
            this.hoveredTable = null;
            this.render();
        });
    }
    
    getMousePos(e) {
        const rect = this.canvas.getBoundingClientRect();
        return {
            x: (e.clientX - rect.left - this.config.padding) / this.scale,
            y: (e.clientY - rect.top - this.config.padding) / this.scale
        };
    }
    
    findTableAtPosition(pos) {
        return this.tables.find(table => {
            const tableX = table.x;
            const tableY = table.y;
            const width = this.config.tableWidth;
            const height = this.config.tableHeight;
            
            if (table.shape === 'round') {
                const radius = this.config.roundTableRadius;
                const distance = Math.sqrt(
                    Math.pow(pos.x - tableX, 2) + Math.pow(pos.y - tableY, 2)
                );
                return distance <= radius;
            } else {
                return pos.x >= tableX - width/2 &&
                       pos.x <= tableX + width/2 &&
                       pos.y >= tableY - height/2 &&
                       pos.y <= tableY + height/2;
            }
        });
    }
    
    handleMouseMove(e) {
        const pos = this.getMousePos(e);
        const table = this.findTableAtPosition(pos);
        
        if (this.hoveredTable !== table) {
            this.hoveredTable = table;
            this.render();
            
            // Update cursor
            this.canvas.style.cursor = table ? 'pointer' : 'default';
            
            // Show tooltip if table found
            if (table) {
                this.showTooltip(table, e.clientX, e.clientY);
            } else {
                this.hideTooltip();
            }
        }
    }
    
    handleClick(e) {
        const pos = this.getMousePos(e);
        const table = this.findTableAtPosition(pos);
        
        if (table && !table.is_reserved) {
            this.selectedTable = this.selectedTable === table ? null : table;
            this.render();
            this.onTableSelect(this.selectedTable);
        }
    }
    
    showTooltip(table, x, y) {
        let tooltip = document.getElementById('table-tooltip');
        if (!tooltip) {
            tooltip = document.createElement('div');
            tooltip.id = 'table-tooltip';
            tooltip.className = 'table-tooltip';
            document.body.appendChild(tooltip);
        }
        
        tooltip.innerHTML = `
            <h4>Table ${table.table_number}</h4>
            <p>Capacity: ${table.capacity} people</p>
            <p>Status: ${table.is_reserved ? 'Reserved' : 'Available'}</p>
            ${table.is_vip ? '<p>VIP Table</p>' : ''}
        `;
        
        tooltip.style.left = `${x + 10}px`;
        tooltip.style.top = `${y + 10}px`;
        tooltip.style.display = 'block';
    }
    
    hideTooltip() {
        const tooltip = document.getElementById('table-tooltip');
        if (tooltip) {
            tooltip.style.display = 'none';
        }
    }
    
    drawTable(table) {
        const x = table.x;
        const y = table.y;
        
        // Determine table color
        let color = this.config.colors.available;
        if (table === this.selectedTable) {
            color = this.config.colors.selected;
        } else if (table === this.hoveredTable) {
            color = this.config.colors.hovered;
        } else if (table.is_reserved) {
            color = this.config.colors.reserved;
        } else if (table.is_vip) {
            color = this.config.colors.vip;
        }
        
        this.ctx.save();
        this.ctx.translate(this.config.padding, this.config.padding);
        this.ctx.scale(this.scale, this.scale);
        
        // Draw table shape
        this.ctx.fillStyle = color;
        this.ctx.strokeStyle = '#000000';
        this.ctx.lineWidth = 2;
        
        if (table.shape === 'round') {
            this.ctx.beginPath();
            this.ctx.arc(x, y, this.config.roundTableRadius, 0, Math.PI * 2);
            this.ctx.fill();
            this.ctx.stroke();
        } else {
            const width = this.config.tableWidth;
            const height = this.config.tableHeight;
            this.ctx.fillRect(x - width/2, y - height/2, width, height);
            this.ctx.strokeRect(x - width/2, y - height/2, width, height);
        }
        
        // Draw table number
        this.ctx.fillStyle = this.config.colors.text;
        this.ctx.font = '16px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(table.table_number.toString(), x, y);
        
        this.ctx.restore();
    }
    
    render() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw all tables
        this.tables.forEach(table => this.drawTable(table));
    }
    
    updateAvailability(availability) {
        this.tables.forEach(table => {
            table.is_reserved = !availability[table.id];
        });
        this.render();
    }
}
