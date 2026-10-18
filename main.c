#include <stdio.h>
#include <string.h>

size_t	ft_strlcat(char *dst, const char *src, size_t dstsize)
{
	size_t	i;
	size_t	ld;
	size_t	ls;
	size_t	j;

	i = 0;
	ls = ft_strlen(src);
	if (!dst && dstsize == 0)
		return (ls);
	ld = ft_strlen(dst);
	j = ld;
	if (dstsize <= ld)
		return (ls + dstsize);
	while (j < dstsize - 1 && src[i])
	{
		dst[j] = src[i];
		i++;
		j++;
	}
	dst[j] = '\0';
	return (ld + ls);

}
int main()
{
}  