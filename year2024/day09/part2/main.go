package main

import (
	"bufio"
	"fmt"
	"os"
)

type File struct {
	id, size int
	moved    bool
}

type Block struct {
	files []File
	free  int
}

func (b *Block) getMovableFile() *File {
	if len(b.files) == 1 && b.files[0].moved == false {
		return &b.files[0]
	} else {
		return nil
	}
}

func (b *Block) movable() bool {
	return b.free == 0 && len(b.files) == 1
}

func (b *Block) fits(f *File) bool {
	return b.free >= f.size
}

func (b *Block) add(f *File) {
	if b.free < f.size {
		panic("Not enough free space")
	}
	b.files = append(b.files, *f)
	b.free -= f.size
	f.moved = true
}

func (b *Block) freeUp() {
	if len(b.files) != 1 {
		panic("Freeing up a block with more than 1 file")
	}
	b.free = b.files[0].size
	b.files = []File{}
}

// Prints in the same format as in the task specification
func printDisk(d []Block) {
	for _, b := range d {
		for _, f := range b.files {
			for i := 0; i < f.size; i++ {
				fmt.Print(f.id)
			}
		}

		for i := 0; i < b.free; i++ {
			fmt.Print(".")
		}
	}

	fmt.Println()
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	line := scanner.Text()

	disk := []Block{}

	fileId := 0
	for i := 0; i < len(line); i++ {
		n := int(line[i]) - int('0')

		var block Block
		if i%2 == 0 {
			// file block
			block = Block{files: []File{{id: fileId, size: n}}, free: 0}
			fileId++
		} else {
			block = Block{files: []File{}, free: n}
		}
		disk = append(disk, block)
	}

	for fileIndex := len(disk) - 1; fileIndex >= 0; fileIndex-- {
		movableFile := disk[fileIndex].getMovableFile()
		if movableFile == nil {
			continue
		}

		// find empty space from front
		emptySpaceIndex := 0
		for ; emptySpaceIndex < fileIndex && !disk[emptySpaceIndex].fits(movableFile); emptySpaceIndex++ {
		}

		if emptySpaceIndex >= fileIndex {
			continue
		}

		// move
		disk[emptySpaceIndex].add(movableFile)
		disk[fileIndex].freeUp()
	}

	checksum := 0
	spaceId := 0
	for i := 0; i < len(disk); i++ {
		for _, f := range disk[i].files {
			for j := 0; j < f.size; j++ {
				checksum += spaceId * f.id
				spaceId++
			}
		}

		spaceId += disk[i].free
	}

	fmt.Println(checksum)
}
