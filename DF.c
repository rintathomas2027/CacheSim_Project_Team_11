#include <stdio.h>

int findLRU(int time[], int n) {
    int min = time[0], pos = 0;

    for (int i = 1; i < n; i++) {
        if (time[i] < min) {
            min = time[i];
            pos = i;
        }
    }
    return pos;
}

int main() {
    int frames, pages;
    int pageFaults = 0, counter = 0;

    printf("Enter number of frames: ");
    scanf("%d", &frames);

    printf("Enter number of pages: ");
    scanf("%d", &pages);

    int page[pages], frame[frames], time[frames];

    printf("Enter page reference string:\n");
    for (int i = 0; i < pages; i++)
        scanf("%d", &page[i]);

    for (int i = 0; i < frames; i++) {
        frame[i] = -1;   // empty frame
        time[i] = 0;
    }

    printf("\nPage\tFrames\n");

    for (int i = 0; i < pages; i++) {
        int flag = 0;

        // Check if page is already in frame
        for (int j = 0; j < frames; j++) {
            if (frame[j] == page[i]) {
                counter++;
                time[j] = counter;
                flag = 1;
                break;
            }
        }

        // If page fault
        if (flag == 0) {
            int pos;
            if (i < frames) {
                pos = i;
            } else {
                pos = findLRU(time, frames);
            }

            frame[pos] = page[i];
            counter++;
            time[pos] = counter;
            pageFaults++;
        }

        // Display frames
        printf("%d\t", page[i]);
        for (int j = 0; j < frames; j++) {
            if (frame[j] != -1)
                printf("%d ", frame[j]);
            else
                printf("- ");
        }
        printf("\n");
    }

    printf("\nTotal Page Faults = %d\n", pageFaults);

    return 0;
}
