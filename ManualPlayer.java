import java.util.*;
import java.io.PrintWriter;


public class ManualPlayer{

    String action_file;

    // ---State---
    Integer n;
    Integer[] centralTiles;
    List<Integer[]> playersStacks;
    Integer[]  dicesOwn;
    Integer[]  dicesThrown;
    String[]  choices;

    public ManualPlayer(List<String> game_state){
        action_file     = game_state.get(0);
        choices         = game_state.get(1).split(" ");
        dicesOwn        = convert(game_state.get(2).split(" "));
        dicesThrown     = convert(game_state.get(3).split(" "));
        centralTiles    = convert(game_state.get(4).split(" "));
        n               = Integer.parseInt(game_state.get(5));
        playersStacks   = new ArrayList<Integer[]>();
        for(int i=0; i<n; i++){
            playersStacks.set(i, convert(game_state.get(6+i).split(" ")));
        }
    }

    public String getAction(){
        display();
        Scanner sc= new Scanner(System.in); //System.in is a standard input stream.
        System.out.println("Write your action : ");
        String action = sc.nextLine(); //reads string.
        while(!Arrays.asList(choices).contains(action)){
            System.out.println("Write a correct action : ");
            action = sc.nextLine();
        }
        return action;
    }

    public Integer[] convert(String[] sTab){
        Integer[] iTab = new Integer[sTab.length];
        for(int i=0; i<sTab.length; i++){
            iTab[i] = Integer.parseInt(sTab[i]);
        }
        return iTab;
    }

    public void display(){
        System.out.println("Turn " + action_file.charAt(0));
        System.out.println("Player " + action_file.charAt(3));
        System.out.println("Throw "+ action_file.charAt(5));
        System.out.println("central tiles : " + centralTiles.toString());
        System.out.println("players stacks : ");
        for(int i=0; i<playersStacks.size(); i++){
            System.out.println(playersStacks.get(i).toString());
        }
        System.out.println("dices own : " + dicesOwn.toString());
        System.out.println("dices thrown : " + dicesThrown.toString());
        System.out.println("choices : " + choices.toString());
    }

    public static void main( String[] argv ) throws Exception {
        List<String>  game_state = new ArrayList<String>();
        Scanner sc = new Scanner(System.in);
        int k = 0;
        while(sc.hasNextLine()) {
            game_state.set(k, sc.nextLine().strip());
            k++;
        }

        ManualPlayer MP = new ManualPlayer(game_state);
        String action = MP.getAction();
        PrintWriter file = new PrintWriter(MP.action_file);
        file.println(action);
    }
}











