import javax.swing.*;
import javax.swing.border.TitledBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.LinkedList;

public class SetAssociativeCacheGUI extends JFrame {

    // --- Configuration ---
    private static final int NUM_SETS = 4; // Number of Rows
    private static final int WAYS = 2;     // Number of Columns (2-way associative)

    // --- GUI Components ---
    private BlockPanel[][] cacheGrid;      // The 2D visual grid
    private JTextArea logArea;             // To show the math/logic steps
    private JTextField addressField;
    private JTextField dataField;
    
    // --- Cache Data Structures (Logic) ---
    // We use a simple counter for FIFO replacement for this demo
    private int[] replacementCounters; 

    public SetAssociativeCacheGUI() {
        setTitle("Set Associative Mapping Visualizer");
        setSize(800, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout(10, 10));

        replacementCounters = new int[NUM_SETS];

        // 1. TOP PANEL: Controls
        JPanel controlPanel = new JPanel(new FlowLayout());
        addressField = new JTextField(10);
        dataField = new JTextField(10);
        JButton writeBtn = new JButton("Write to Cache");
        
        controlPanel.add(new JLabel("Memory Address (Int):"));
        controlPanel.add(addressField);
        controlPanel.add(new JLabel("Data (String):"));
        controlPanel.add(dataField);
        controlPanel.add(writeBtn);

        add(controlPanel, BorderLayout.NORTH);

        // 2. CENTER PANEL: The 2D Cache Grid
        JPanel gridPanel = new JPanel(new GridLayout(NUM_SETS, 1, 10, 10)); // Rows of Sets
        gridPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        
        cacheGrid = new BlockPanel[NUM_SETS][WAYS];

        for (int i = 0; i < NUM_SETS; i++) {
            // Create a panel for the Set (Row)
            JPanel setPanel = new JPanel(new GridLayout(1, WAYS, 10, 0));
            setPanel.setBorder(BorderFactory.createTitledBorder(
                    BorderFactory.createLineBorder(Color.GRAY), "Set " + i));
            
            for (int j = 0; j < WAYS; j++) {
                BlockPanel block = new BlockPanel(j);
                cacheGrid[i][j] = block;
                setPanel.add(block);
            }
            gridPanel.add(setPanel);
        }
        
        // Wrap grid in scroll pane
        add(new JScrollPane(gridPanel), BorderLayout.CENTER);

        // 3. BOTTOM PANEL: Logs
        logArea = new JTextArea(8, 50);
        logArea.setEditable(false);
        logArea.setFont(new Font("Monospaced", Font.PLAIN, 12));
        add(new JScrollPane(logArea), BorderLayout.SOUTH);

        // 4. Action Listener Logic
        writeBtn.addActionListener(e -> processMemoryAccess());
        
        // Initialize with default values for quick testing
        addressField.setText("0");
        dataField.setText("A");
    }

    private void processMemoryAccess() {
        try {
            int address = Integer.parseInt(addressField.getText());
            String data = dataField.getText();

            // --- The Core Math ---
            int setIndex = address % NUM_SETS;
            int tag = address / NUM_SETS;

            log("-------------------------------");
            log("Request: Address " + address + " | Data: " + data);
            log("Mapping: " + address + " % " + NUM_SETS + " = Set " + setIndex);
            log("Tag Calc: " + address + " / " + NUM_SETS + " = Tag " + tag);

            // 1. Check for HIT in the specific row (Set)
            boolean hit = false;
            for (int col = 0; col < WAYS; col++) {
                BlockPanel block = cacheGrid[setIndex][col];
                if (block.isValid && block.tag == tag) {
                    // HIT!
                    block.updateData(tag, data, true);
                    log(" -> HIT in Way " + col + "! Updated data.");
                    resetColors(setIndex, col); // Highlight only this block
                    hit = true;
                    return; 
                }
            }

            // 2. Look for Empty Slot (MISS)
            if (!hit) {
                for (int col = 0; col < WAYS; col++) {
                    BlockPanel block = cacheGrid[setIndex][col];
                    if (!block.isValid) {
                        // Found empty spot
                        block.updateData(tag, data, true);
                        log(" -> MISS. Placed in Empty Way " + col);
                        resetColors(setIndex, col);
                        return;
                    }
                }
            }

            // 3. Set is Full - Eviction (Round Robin)
            int victimCol = replacementCounters[setIndex];
            log(" -> MISS & FULL. Evicting Way " + victimCol + " (Round Robin)");
            
            BlockPanel victim = cacheGrid[setIndex][victimCol];
            victim.updateData(tag, data, true);
            
            // Highlight the change
            resetColors(setIndex, victimCol);
            
            // Increment counter for next time
            replacementCounters[setIndex] = (replacementCounters[setIndex] + 1) % WAYS;

        } catch (NumberFormatException ex) {
            JOptionPane.showMessageDialog(this, "Please enter a valid integer for Address.");
        }
    }

    private void log(String msg) {
        logArea.append(msg + "\n");
        logArea.setCaretPosition(logArea.getDocument().getLength());
    }

    // Helper to dim other cells and highlight the active one
    private void resetColors(int activeSet, int activeWay) {
        for(int i=0; i<NUM_SETS; i++) {
            for(int j=0; j<WAYS; j++) {
                if(i == activeSet && j == activeWay) {
                    cacheGrid[i][j].highlight(true); // Active
                } else {
                    cacheGrid[i][j].highlight(false); // Dim
                }
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new SetAssociativeCacheGUI().setVisible(true);
        });
    }

    // --- Inner Class for Visual Block ---
    class BlockPanel extends JPanel {
        int wayIndex;
        int tag = -1;
        boolean isValid = false;
        
        JLabel tagLabel;
        JLabel dataLabel;
        JLabel statusLabel;

        public BlockPanel(int way) {
            this.wayIndex = way;
            this.setLayout(new GridLayout(3, 1));
            this.setBorder(BorderFactory.createLineBorder(Color.LIGHT_GRAY, 2));
            this.setBackground(new Color(245, 245, 245)); // Default gray

            statusLabel = new JLabel("Way " + way + ": [EMPTY]", SwingConstants.CENTER);
            tagLabel = new JLabel("Tag: -", SwingConstants.CENTER);
            dataLabel = new JLabel("Data: -", SwingConstants.CENTER);

            add(statusLabel);
            add(tagLabel);
            add(dataLabel);
        }

        public void updateData(int tag, String data, boolean valid) {
            this.tag = tag;
            this.isValid = valid;
            tagLabel.setText("Tag: " + tag);
            dataLabel.setText("Data: " + data);
            statusLabel.setText("Way " + wayIndex + ": [OCCUPIED]");
        }

        public void highlight(boolean active) {
            if (active) {
                this.setBackground(new Color(144, 238, 144)); // Light Green for Activity
                this.setBorder(BorderFactory.createLineBorder(new Color(0, 100, 0), 3));
            } else {
                this.setBackground(isValid ? Color.WHITE : new Color(245, 245, 245));
                this.setBorder(BorderFactory.createLineBorder(Color.LIGHT_GRAY, 1));
            }
        }
    }
}