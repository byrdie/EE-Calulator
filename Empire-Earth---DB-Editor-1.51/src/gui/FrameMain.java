package gui;

import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.io.File;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.SwingConstants;
import javax.swing.WindowConstants;
import javax.swing.filechooser.FileNameExtensionFilter;

import datmanager.Core;
import datmanager.DatFile;
import datstructure.DatStructure;
import gui.components.JButtonDat;
import gui.components.JButtonRed;
import gui.components.JScrollPaneRed;
import gui.ui.EEScrollBarUI;
import gui.ui.GridBagConstraintsExtended;
import gui.ui.GridBagLayoutExtended;


/**
 * The main window
 * @author MarcoForlini
 */
public class FrameMain extends JFrame implements WindowListener {
	
	private static final long serialVersionUID = 1973882004055163035L;
	
	/** Text used in the ABOUT dialog */
	public static final String S_ABOUT = "EE - DB Editor\nVersion: " + Core.VERSION + "\nCreated by Forlins & the EE Heaven community   \nGNU General Public License v3   ";

	/** Singletone intance of FrameMain */
	public static final FrameMain instance = new FrameMain();
	
	
	
	/** After the first load, the load dialog won't enable anymore all files by default */
	public boolean firstLoad = true;
	private JPanel contentPane = new JPanel();
	private final JPanel scrollPanePanel = new JPanel();
	private final JScrollPane scrollPane = new JScrollPaneRed(scrollPanePanel);
	private final JButton dbLoad;


	
	/** Initialize */
	{
		JLabel image = new JLabel(GUI.IMAGE_LOGO);
		JLabel scrollPaneLabel = new JLabel("Loaded data");
		scrollPaneLabel.setHorizontalAlignment(SwingConstants.CENTER);
		JPanel labelContainer = new JPanel();
		labelContainer.add(scrollPaneLabel);
		labelContainer.setOpaque(false);
		dbLoad = new JButtonRed("Load dat file");
		JButton dbInfo = new JButtonRed("About");
		dbLoad.addActionListener(this::loadFiles);
		dbInfo.addActionListener(evt -> JOptionPane.showMessageDialog(this, S_ABOUT, "About", JOptionPane.INFORMATION_MESSAGE, GUI.IMAGE_EE_HEAVEN_LOGO));

		scrollPane.getVerticalScrollBar().setUI(new EEScrollBarUI());
		scrollPane.getHorizontalScrollBar().setUI(new EEScrollBarUI());
		scrollPane.getVerticalScrollBar().setUnitIncrement(6);
		scrollPane.setColumnHeaderView(labelContainer);
		scrollPane.setOpaque(false);
		scrollPane.getViewport().setOpaque(false);
		scrollPane.getColumnHeader().setOpaque(false);
		scrollPane.setVisible(false);
		
		scrollPanePanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
		scrollPanePanel.setOpaque(false);
		scrollPaneLabel.setOpaque(false);


		contentPane.setBackground(GUI.COLOR_UI_BACKGROUND);
		contentPane.setLayout(new GridBagLayoutExtended(new int[]{680, 0}, new int[]{280, 50, 50}, new double[]{0, 1.0}, new double[]{1.0, 0.0, 0.0}));
		contentPane.add(image, new GridBagConstraintsExtended(5, 25, 5, 25, 0, 0));
		contentPane.add(dbLoad, new GridBagConstraintsExtended(10, 25, 5, 25, 0, 1));
		contentPane.add(dbInfo, new GridBagConstraintsExtended(5, 25, 10, 25, 0, 2));

		setContentPane(contentPane);
		setBounds(Core.getBounds(this, 680, 400));
		setDefaultCloseOperation(WindowConstants.DO_NOTHING_ON_CLOSE);
		setResizable(false);
		setAutoRequestFocus(false);
		setIconImage(GUI.IMAGE_ICON.getImage());
		addWindowListener(this);
	}
	
	
	/**
	 * Create and show the new window
	 */
	public FrameMain () {
		super("Empire Earth - " + (Core.AOC ? "Art of Conquest -" : "") + "DB Editor");
	}
	

	/**
	 * Select a directory, starting from the given one
	 * @param fromDirectory		The starting directory
	 * @return					The choosen directory
	 */
	public static File selectDirectory(File fromDirectory){
		JFileChooser fileChooser = new JFileChooser(fromDirectory != null ? fromDirectory : new File("."));
		fileChooser.setAcceptAllFileFilterUsed(false);
		fileChooser.setFileHidingEnabled(false);
		fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
		fileChooser.addChoosableFileFilter(new FileNameExtensionFilter("EE \"db\" folder", "*"));
		fileChooser.setDialogTitle("Select the folder which contains the EE dat files");
		fileChooser.setDialogType(JFileChooser.OPEN_DIALOG);
		int response = fileChooser.showDialog(null, "Select directory");

		if (response == JFileChooser.APPROVE_OPTION) {
			File selectedDirectory = fileChooser.getSelectedFile();
			if (selectedDirectory.exists()){
				return selectedDirectory;
			}
		}
		return null;
	}

	

	/**
	 * Load all selected files
	 * @param evt	The action event
	 */
	public void loadFiles(ActionEvent evt){
		File selectedDirectory = null;
		List<DatFile> allFiles;
		List<Boolean> loaded;
		do{
			selectedDirectory = selectDirectory(selectedDirectory);
			if (selectedDirectory == null){
				return;
			}
			String selectedDirectoryPath = selectedDirectory.getPath();
			DatStructure[] allStructures = Core.AOC ? DatStructure.ALL_AOC : DatStructure.ALL_VANILLA;
			allFiles = new ArrayList<>(allStructures.length);
			loaded = new ArrayList<>(allFiles.size());
			for(DatStructure datStructure : allStructures){
				DatFile datFile = new DatFile(selectedDirectoryPath + File.separatorChar + datStructure.fileName, datStructure);
				if (datFile.exists()){
					allFiles.add(datFile);
					if (datFile.isLoaded()){
						loaded.add(true);
					} else {
						loaded.add(false);
					}
				}
			}
			if (allFiles.isEmpty()){
				JOptionPane.showMessageDialog(this, "There's no dat file in this directory!", "Error", JOptionPane.ERROR_MESSAGE, GUI.IMAGE_ICON);
			} else {
				break;
			}
		} while (true);

		DialogSelectFiles frameFiles = new DialogSelectFiles(this, allFiles, loaded, firstLoad);
		List<DatFile> files = frameFiles.getFilesToLoad();
		if (files == null || files.isEmpty()){
			return;
		}
		
		Core.loadFiles(this, files, (data) -> {
			DatFile.LOADED.addAll(data);
			int gridRows = Math.max(10, DatFile.LOADED.size());
			scrollPanePanel.setVisible(false);
			scrollPanePanel.removeAll();
			scrollPanePanel.setLayout(new GridLayout((int) Math.ceil(gridRows/3f), 3, 6, 6));
			for (DatFile datFile : DatFile.LOADED.parallelStream().sorted().toArray(DatFile[]::new)){
				scrollPanePanel.add(new JButtonDat(this, datFile));
			}
			if (firstLoad) {
				contentPane.add(scrollPane, new GridBagConstraintsExtended(10, 10, 10, 10, 1, 0, 0, 3));
				firstLoad = false;
			}
			scrollPanePanel.setVisible(true);
			scrollPanePanel.revalidate();
			scrollPane.setVisible(true);
			setBounds(Core.getBounds(this, 1280, 0.7));
		}, ()->{/*Do nothing*/});
	}




	@Override
	public void windowClosing (WindowEvent e) {
		Set<DatFile> unsaved = new HashSet<>();
		for (DatFile datFile : DatFile.LOADED){
			if (datFile.isLoaded() && datFile.isUnsaved()){
				unsaved.add(datFile);
			}
		}
		if (!unsaved.isEmpty()){
			final String[] choices = {"Save", "Don't save", "Cancel"};
			switch (JOptionPane.showOptionDialog(this, "There are unsaved changes. Do you want to save all unsaved files?", "Unsaved changes", JOptionPane.YES_NO_CANCEL_OPTION, JOptionPane.QUESTION_MESSAGE, GUI.IMAGE_ICON, choices, choices[0])){
				case 2:
				case JOptionPane.CLOSED_OPTION:
					return;
				case 0:
					unsaved.forEach(datFile -> Core.saveFile(this, datFile));
					//Don't do break. We're going to exit anyway.
				case 1:
					System.exit(0);
			}
		} else {
			System.exit(0);
		}
	}

	@Override public void windowOpened (WindowEvent e) {/*Do nothing*/}
	@Override public void windowClosed (WindowEvent e) {/*Do nothing*/}
	@Override public void windowIconified (WindowEvent e) {/*Do nothing*/}
	@Override public void windowDeiconified (WindowEvent e) {/*Do nothing*/}
	@Override public void windowActivated (WindowEvent e) {/*Do nothing*/}
	@Override public void windowDeactivated (WindowEvent e) {/*Do nothing*/}
	
}


