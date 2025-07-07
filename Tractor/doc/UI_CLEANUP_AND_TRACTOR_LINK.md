# UI Cleanup and Tractor Link Integration

## Changes Made

### 1. Removed Debug Blade Button
- **Removed**: "Debug: Show Available Blades" button from the right column
- **Rationale**: Cleanup of debugging features for production use
- **Impact**: Cleaner, more professional UI layout

### 2. Replaced Tractor Jobs Table with Web Link
- **Removed**: 
  - Tractor Nuke Jobs table display
  - Job refresh functionality  
  - `updateJobList()` method
  - `get_nuke_jobs()` function
  - Table widget and refresh button

- **Added**: 
  - Clickable hyperlink to Tractor web interface
  - URL: `http://10.31.240.8/tv/`
  - Styled link with hover effects
  - Informational text about monitoring capabilities

### 3. UI Layout Improvements
- **New Tractor Monitor Section**:
  - Clean, centered layout with proper spacing
  - Styled clickable link with visual feedback
  - Informational text explaining functionality
  - Professional appearance with border and hover effects

## Benefits

### 1. Simplified Interface
- Removed complex table logic that could fail
- Eliminated network dependencies for job listing
- Faster UI loading without job queries
- Cleaner, more focused layout

### 2. Better User Experience  
- Direct access to full Tractor web interface
- More comprehensive job monitoring capabilities
- No need for custom job refresh logic
- External browser window for better monitoring workflow

### 3. Reduced Complexity
- Less code to maintain
- Fewer potential failure points
- No custom Tractor query dependencies
- Simplified error handling

## Implementation Details

### Hyperlink Styling
```python
self.tractorLink = QtWidgets.QLabel('<a href="http://10.31.240.8/tv/" style="color: #4A90E2; text-decoration: none; font-size: 13px;">🔗 Open Tractor Web Interface</a>')
self.tractorLink.setOpenExternalLinks(True)
```

### CSS Styling
- Professional blue color scheme (`#4A90E2`)
- Hover effects for visual feedback
- Border and background for clear definition
- Responsive design with proper padding

### Layout Structure
```
Middle Column (Tractor Monitor):
├── Stretch (top spacing)
├── Title Label: "Tractor Job Monitor"
├── Clickable Link: "🔗 Open Tractor Web Interface"  
├── Info Text: Description of functionality
└── Stretch (bottom spacing)
```

## User Workflow

1. **Job Submission**: User configures and submits jobs as before
2. **Job Monitoring**: Click the Tractor link to open web interface
3. **External Monitoring**: Use full Tractor web UI for:
   - Job status tracking
   - Log file viewing
   - Farm activity monitoring
   - Advanced job management

## Technical Notes

- Link opens in system default browser
- No authentication required (handled by browser)
- Full Tractor web interface functionality available
- Compatible with all operating systems
- No additional network requests from Nuke

The changes result in a cleaner, more reliable UI that leverages the existing Tractor web interface rather than trying to replicate its functionality within the Nuke panel.
