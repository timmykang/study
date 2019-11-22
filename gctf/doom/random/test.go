package main
import "fmt"
func main(){
	nums := make([]int, 56)
	for i, _ := range nums{
		nums[i] = i/2
	}
	fmt.Println(nums)
}
