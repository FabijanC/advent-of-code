import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.Arrays;

class Sol2 {
    public static void main(String[] args) throws FileNotFoundException {
        File f = new File(args[0]);
        String input = null;
        try (Scanner sc = new Scanner(f)) {
            input = sc.nextLine().trim();
        }
        int offset = Integer.parseInt(input.substring(0, 7));

        int repeatTimes = 10000;
        int signal[] = new int[repeatTimes*input.length()];
        int signalIndex = 0;
        for (int i = 0; i < repeatTimes; ++i) {
            for (int j = 0; j < input.length(); ++j) {
                signal[signalIndex++] = input.charAt(j) - '0';
            }
        }

        for (int step = 0; step < 100; ++step) {
            int[] prefixSum = new int[signal.length+1];
            prefixSum[0] = 0;
            for (int i = 1; i <= signal.length; ++i) {
                prefixSum[i] = prefixSum[i-1] + signal[i-1];
            }

            int[] newSignal = new int[signal.length];
            for (int i = 0; i < signal.length; ++i) {
                int sign = 1;
                int newSignalVal = 0;
                for (int j = i; j < signal.length; j += 2*(i+1)) {
                    int tmp = prefixSum[Math.min(j+i+1, signal.length)] - prefixSum[j];
                    newSignalVal += sign * tmp;
                    sign *= -1;
                }
                newSignal[i] = Math.abs(newSignalVal) % 10;
            }
            signal = newSignal;
            for (int i = offset; i < offset+8; ++i) {
                System.out.print(signal[i]);
            }
            System.out.println();
        }
    }
}